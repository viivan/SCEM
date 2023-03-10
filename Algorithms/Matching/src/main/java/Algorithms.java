
import com.hp.hpl.jena.ontology.*;
import com.hp.hpl.jena.rdf.model.*;
import net.didion.jwnl.data.IndexWord;
import net.didion.jwnl.data.POS;
import net.didion.jwnl.data.PointerUtils;
import net.didion.jwnl.data.Synset;
import net.didion.jwnl.data.list.PointerTargetNodeList;
import net.didion.jwnl.data.list.PointerTargetTree;
import net.didion.jwnl.data.list.PointerTargetTreeNode;
import net.didion.jwnl.data.relationship.Relationship;
import net.didion.jwnl.dictionary.Dictionary;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.mindswap.owl.OWLFactory;
import org.mindswap.owl.OWLIndividual;
import org.mindswap.owl.OWLKnowledgeBase;
import org.mindswap.owls.process.InputList;
import org.mindswap.owls.process.Process;
import org.mindswap.owls.service.Service;
import net.didion.jwnl.*;
import java.io.*;
import java.net.URI;
import java.util.*;

public class Algorithms {

    /** 
     * 语义相似度计算
     * @param A 本体概念A
     * @param B 本体概念B
     * @param PD 样本训练出的条件概率分布列
     * @param alpha 样本训练出的调整因子
     * @param beta 样本训练出的调整因子
     * @return 本体概念A与B的语义相似度
     */
    public static double conceptSim(MyOntology A, MyOntology B, double PD[][][], double alpha, double beta) {
        double simConcept = 0;
        // 属性相似阈值
        double eta = 0.8;
        if (A.equals(B)) {
            simConcept = 1;
        } else if (B.contains(A)) {
            simConcept = B.getSize() / A.getSize();
        } else if (A.contains(B)) {
            simConcept = A.getSize() / B.getSize();
        } else {
            int i = 0;
            if (A.getProperties() != null && B.getProperties() != null) {
                for (OntProperty propertyInA : A.getProperties()) {
                    for (OntProperty propertyInB : B.getProperties()) {
                        ArrayList<Integer> LD = computeFeature(propertyInA.getLocalName(), propertyInB.getLocalName());
                        if (LD != null) {
                            double v1 = PD[0][LD.get(0)][0];
                            double v2 = PD[1][LD.get(1)][0];
                            double v3 = PD[0][LD.get(0)][1];
                            double v4 = PD[1][LD.get(1)][1];
                            double simWord = (alpha * v1 * v2) / (alpha * v1 * v2 + beta * v3 * v4);
                            if (simWord >= eta) {
                                i++;
                                break;
                            }
                        } else {
                            return 0;
                        }
                    }
                }
                simConcept = i / (A.getSize() + B.getSize() - i);
            } else if (A.getProperties() == null && B.getProperties() == null) {
                ArrayList<Integer> LD = computeFeature(A.getOntClass().getLocalName(), B.getOntClass().getLocalName());
                if (LD != null) {
                    double v1 = PD[0][LD.get(0)][0];
                    double v2 = PD[1][LD.get(1)][0];
                    double v3 = PD[0][LD.get(0)][1];
                    double v4 = PD[1][LD.get(1)][1];
                    double simWord = (alpha * v1 * v2) / (alpha * v1 * v2 + beta * v3 * v4);
                    if (simWord >= eta) {
                        i++;
                    }
                } else {
                    return 0;
                }
                simConcept = i / (A.getSize() + B.getSize() - i);
            } else {
                // 不为空
                MyOntology C = (A.getProperties() == null ? B : A);
                // 为空
                MyOntology D = (A.getProperties() == null ? A : B);
                for (OntProperty property : C.getProperties()) {
                    ArrayList<Integer> LD = computeFeature(property.getLocalName(), D.getOntClass().getLocalName());
                    if (LD != null) {
                        double v1 = PD[0][LD.get(0)][0];
                        double v2 = PD[1][LD.get(1)][0];
                        double v3 = PD[0][LD.get(0)][1];
                        double v4 = PD[1][LD.get(1)][1];
                        double simWord = (alpha * v1 * v2) / (alpha * v1 * v2 + beta * v3 * v4);
                        if (simWord >= eta) {
                            i++;
                            break;
                        }
                    } else {
                        return 0;
                    }
                }
                simConcept = i / (A.getSize() + B.getSize() - i);
            }

        }

        return simConcept;
    }

    /**
     * 语义相似度计算 重载 使用默认值
     * @param A 本体概念A
     * @param B 本体概念B
     * @return 本体概念A与B的语义相似度
     */
    public static double conceptSim(MyOntology A, MyOntology B) {
        return conceptSim(A, B, new double[2][2][2], 0.8, 0.8);
    }

    /**
     * 输入相似度计算
     * @param input1 服务S1的输入
     * @param input2 服务S2的输入
     * @return 服务S1，S2的输入相似度
     */
    public static double inputSim(ArrayList<MyOntology> input1, ArrayList<MyOntology> input2) {
        if (input1.size() == 0 || input2.size() == 0) {
            return 0;
        }
        int d = input1.size() - input2.size();

        double sumInSim = 0;
        ArrayList<MyOntology> inputLong;
        ArrayList<MyOntology> inputShort;
        if (d <= 0) {
            inputShort = input1;
            inputLong = input2;
        } else {
            inputShort = input2;
            inputLong = input1;
        }
        double[] inSim = new double[inputLong.size()];
        int i = 0;

        for (Iterator<?> iter = input1.iterator(); iter.hasNext(); ) {
            MyOntology e1 = (MyOntology) iter.next();
            for (Iterator<?> iter2 = input2.listIterator(); iter2.hasNext(); ) {
                MyOntology e2 = (MyOntology) iter2.next();
                inSim[i] = max(inSim[i], conceptSim(e1, e2));
            }
            i++;
        }

        double simInput = (sum(inSim) / inputShort.size()) * (1 - (d / inputLong.size()));

        return simInput;
    }

    /**
     * 输出相似度计算
     * @param output1 服务S1的输出
     * @param output2 服务S2的输出
     * @return 服务S1，S2的输出相似度
     */
    public static double outputSim(ArrayList<MyOntology> output1, ArrayList<MyOntology> output2) {
        if (output1.size() == 0 || output2.size() == 0) {
            return 0;
        }
        int d = output1.size() - output2.size();

        double sumInSim = 0;
        ArrayList<MyOntology> outputLong;
        ArrayList<MyOntology> outputShort;
        if (d <= 0) {
            outputShort = output1;
            outputLong = output2;
        } else {
            outputShort = output2;
            outputLong = output1;
        }
        double[] outSim = new double[outputLong.size()];
        int i = 0;
        for (Iterator<?> iter = output1.iterator(); iter.hasNext(); ) {
            MyOntology e1 = (MyOntology) iter.next();
            for (Iterator<?> iter2 = output2.iterator(); iter.hasNext(); ) {
                MyOntology e2 = (MyOntology) iter2.next();
                outSim[i] = max(outSim[i], conceptSim(e1, e2));
            }
            i++;
        }

        double simOutput = (sum(outSim) / outputShort.size()) * (1 - (d / outputLong.size()));

        return simOutput;
    }

    /**
     * DBSCAN服务聚类算法
     * @param services 服务样本集
     * @param eps 邻域参数
     * @param minPts 邻域参数
     * @return 簇划分C
     */
    public static ArrayList<ArrayList<MyService>> dbscan(ArrayList<MyService> services, double eps, double minPts) {
        ArrayList<MyService> gamma = (ArrayList<MyService>) services.clone();
        Map<MyService, ArrayList<MyService>> nEps = new HashMap<MyService, ArrayList<MyService>>();
        ArrayList<ArrayList<MyService>> c = new ArrayList<ArrayList<MyService>>();
        while (!gamma.isEmpty()) {
            MyService s0 = gamma.get(0);
            gamma.remove(0);
            nEps.put(s0, new ArrayList<MyService>());

            for (int i = 0; i < gamma.size(); i++) {
                MyService si = gamma.get(i);
                if (functionalSim(s0,si) <= eps) {
                    nEps.get(s0).add(si);
                }
            }

            ArrayList<MyService> ck = new ArrayList<MyService>();
            if (nEps.get(s0).size() > minPts) {
                ck.add(s0);
                for (MyService s0t : nEps.get(s0)) {
                    nEps.put(s0t, new ArrayList<MyService>());
                    if (gamma.contains(s0t)) {
                        gamma.remove(s0t);
                        for (int j = 0; j < gamma.size(); j++) {
                            MyService sj = gamma.get(j);
                            if (functionalSim(s0t, sj) <= eps) {
                                nEps.get(s0t).add(sj);
                            }
                        }

                        if (nEps.get(s0t).size() > minPts) {
                            nEps.get(s0).addAll(0, nEps.get(s0t));
                            if (!c.contains(s0t)) {
                                ck.add(s0t);
                            }
                        }
                    }
                }

                c.add(ck);
            }

        }

        return c;
    }

    /**
     * 服务过滤算法
     * @param candidateServices 候选服务
     * @param qoSConstraints QoS约束
     * @return 过滤后的候选服务
     */
    public static ArrayList<MyService> serviceFilter(ArrayList<MyService> candidateServices, HashMap<String, QoSConstraint> qoSConstraints) {
        ArrayList<MyService> resultServices = (ArrayList<MyService>) candidateServices.clone();
        for (MyService s : candidateServices) {
            for (QoSProperty qoSProperty : s.getQoSProperties()) {
                if (qoSConstraints.containsKey(qoSProperty.getName())) {
                    String type = qoSProperty.getQoSCharacteristic().getType();
                    double charValue = qoSProperty.getQoSCharacteristic().getValue();
                    double consValue = qoSConstraints.get(qoSProperty.getName()).getValue();
                    double conf = qoSConstraints.get(qoSProperty.getName()).getConfidence();
                    if (conf != 0) {
                        if (type.equals("benefit") && (charValue < (consValue * conf))) {
                            resultServices.remove(s);
                        } else if (type.equals("cost") && (charValue > (consValue / conf))) {
                            resultServices.remove(s);
                        }
                    }
                    }
                }
            }
        return resultServices;
    }


    /**
     * 服务综合评分计算
     * @param candidateServices 候选服务
     * @param qoSConstraints QoS约束
     * @param w1 功能相似度权重
     * @param w2 QoS评分权重
     * @param sRCT 当前RCT节点服务需求sRCT
     * @return 服务综合得分向量compScore
     */
    public static double[] serviceScore(ArrayList<MyService> candidateServices, HashMap<String, QoSConstraint> qoSConstraints, double w1, double w2, MyService sRCT) {
        double[] qosScore = new double[candidateServices.size()];
        double[] compScore = new double[candidateServices.size()];
        double[][] qosMatrix = new double[candidateServices.size()][10];

        for (int i = 0; i < candidateServices.size(); i++) {
            MyService s = candidateServices.get(i);
            for (int j = 0; j < s.getQoSProperties().size(); j++) {
                qosMatrix[i][j] = s.Normalize(s.getQoSProperties().get(j));
                if (qoSConstraints.containsKey(s.getQoSProperties().get(j).getName())) {
                    qosScore[i] += (qosMatrix[i][j] * qoSConstraints.get(s.getQoSProperties().get(j).getName()).getWeight());
                }
            }

            compScore[i] = w1 * functionalSim(s, sRCT) + w2 * qosScore[i];
        }

        return compScore;
    }


    // 辅助概念类

    /**
     * 计算两个概念（Property）之间的相似度
     * @param name1 输入概念p1
     * @param name2 输入概念p2
     * @return 两个概念之间的相似度
     */
    private static ArrayList<Integer> computeFeature(String name1, String name2) {
        ArrayList<Integer> result = new ArrayList<Integer>();
        // 调用外部python文件
        String exe = "python";
        String command = "src/main/resources/computeFeature.py";
        String arg1 = name1;
        String arg2 = name2;
        String[] commandArr = new String[] {exe, command, arg1, arg2};
        try {
            java.lang.Process process = Runtime.getRuntime().exec(commandArr);
            InputStream is = process.getInputStream();
            DataInputStream dis = new DataInputStream(is);
            String str = dis.readLine();
            process.waitFor();
            String[] strArray = str.split(" ");
            result.add(Integer.parseInt(strArray[0]));
            result.add(Integer.parseInt(strArray[1]));

            return result;
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return null;
    }

    /**
     * 度量两个服务样本之间的距离
     * @param s1 服务1
     * @param s2 服务2
     * @return 样本距离
     */
    private static double functionalSim(MyService s1, MyService s2) {
        return 0.5 * inputSim(s1.getInputs(), s2.getInputs()) + 0.5 * outputSim(s1.getOutputs(), s2.getOutputs());
    }

    /**
     * 度量两个服务样本之间的距离 重载
     * @param s1 服务1
     * @param s2 服务2
     * @param w1 输入权重w1
     * @param w2 输出权重w2
     * @return 样本距离
     */
    private static double functionalSim(MyService s1, MyService s2, double w1, double w2) {
        return w1 * inputSim(s1.getInputs(), s2.getInputs()) + w2 * outputSim(s1.getOutputs(), s2.getOutputs());
    }


    // 功能类

    /**
     * 输出两数中较大的一个
     * @param a 数1
     * @param b 数2
     * @return 较大的数
     */
    private static double max(double a, double b) {
        return (a > b ? a : b);
    }

    /**
     * 数组求和
     * @param array 输入数组
     * @return 数组的和
     */
    private static double sum(double[] array) {
        double result = 0;
        for (int i = 0; i < array.length; i++) {
            result += array[i];
        }

        return result;
    }

    /**
     *  读取OWL文件
     * @param pathname 文件名/文件路径
     * @return OWL文件中包含的class -> 封装为MyOntology类
     */
    public static ArrayList<MyOntology> readOWL(String pathname) {
        ArrayList<MyOntology> result = new ArrayList<MyOntology>();
        OntModel model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
        try {
            model.read(new FileInputStream("src/main/resources/order.owl"), "");
            for (Iterator<?> iter = model.listNamedClasses(); iter.hasNext(); ) {
                result.add(new MyOntology((OntClass) iter.next()));
            }
        } catch (FileNotFoundException fne) {
            fne.printStackTrace();
        }

        return result;
    }

    /**
     * 读取OWLS文件
     * @param pathname 文件名/文件路径
     * @return OWLS文件中包含的service -> 封装为MyService类
     */
    public static MyService readOWLS(String pathname) {
        return new MyService(pathname);
    }


    // MAIN
    public static void main(String[] args) {

        System.out.println(computeFeature("man", "human"));

//        MyService myService1 = readOWLS("src/main/resources/add_order_service.owls");
//        MyService myService2 = readOWLS("src/main/resources/delete_order_service.owls");
//        functionalSim(myService1, myService2);

//        OntModel model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
//        try {
//            model.read(new FileInputStream("src/main/resources/order.owl"), "");
//            for (Iterator<?> iter2 = model.listNamedClasses(); iter2.hasNext(); ) {
//                System.out.println(((OntClass) iter2.next()).getLocalName());
//            }
//        } catch (FileNotFoundException fne) {
//            fne.printStackTrace();
//        }
//
//
//
//        System.out.println(model.listClasses());
//        try {
//            model.read(new FileInputStream("src/main/resources/order.owl"), "");
//        } catch (FileNotFoundException fne) {
//            fne.printStackTrace();
//        }
//
//        System.out.println(model.createClass().getLocalName());

//        OWLKnowledgeBase kb = OWLFactory.createKB();
//        try {
//            Service service = kb.readService(URI.create("file:./src/main/resources/add_order_service.owls"));
//            System.out.println(service.getName());
//        } catch (IOException ioe) {
//            ioe.printStackTrace();
//        }


        //=============================================================
//        SAXReader saxReader = new SAXReader();
//
//        try {
//            Document document = saxReader.read(new File("src/main/resources/add_order_service.owls"));
//            Element root = document.getRootElement();
//            // 此处获取Qos的各种信息
//            root.element("Qos").element("QosProperty").element("qosPropertyName").getText();
//
//            // 此处读取owls文件
//            OWLKnowledgeBase kb = OWLFactory.createKB();
//            Service serv = kb.readService(URI.create("file:./src/main/resources/add_order_service.owls"));
//
//            Process proc = serv.getProcess();
//
//            InputList inputList = proc.getInputs();
//
//            for(Iterator<?> iter = inputList.iterator(); iter.hasNext(); ) {
//                OWLIndividual owlIndividual = (OWLIndividual) iter.next();
//                Resource resource = (Resource) owlIndividual.getImplementation();
//
//                // Resource转OntClass还没搞定！
//                OntModel modelForClass = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
//                modelForClass.setStrictMode(false);
//                OntClass ontClass = modelForClass.createComplementClass("", resource);
////                for (Iterator<?> iter2 = resource.listProperties(); iter2.hasNext(); ) {
////                    Statement stm = (Statement) iter2.next();
////                    ontClass.addSubClass(stm.getSubject());
////                }
//
////                OntModel ontModel = ModelFactory.createOntologyModel(OntModelSpec.RDFS_MEM_RDFS_INF, resource.getModel());
////                ontModel.setStrictMode(false);
////
////                for (Iterator<?> iter2 = ontModel.listNamedClasses(); iter2.hasNext(); ) {
////                    System.out.println(((OntClass) iter2.next()).getLocalName());
////                }
//            }
//
//        } catch (DocumentException de) {
//            de.printStackTrace();
//        }catch (IOException ioe) {
//            ioe.printStackTrace();
//        }

        //====================================================================
//        SAXReader saxReader = new SAXReader();
//        try {
//            Document document = saxReader.read(new File("src/main/resources/add_order_service.owls"));
//            Element root = document.getRootElement();
//            // 此处获取Qos的各种信息
//            for (Iterator<?> iter = root.element("Qos").element("QosProperty").elementIterator(); iter.hasNext(); ) {
//                Element element = (Element) iter.next();
//                System.out.println(element.getName() + " " + element.getText());
//            }
//        } catch (DocumentException e) {
//            e.printStackTrace();
//        }

        //====================================================================
//        SAXReader saxReader = new SAXReader();
//
//        try {
//            Document document = saxReader.read(new File("src/main/resources/add_order_service.owls"));
//            Element root = document.getRootElement();
//            for (Iterator<?> iter = root.element("Qos").elementIterator(); iter.hasNext(); ) {
//                Element element = (Element) iter.next();
//                if (element.getName().equals("QosProperty")) {
//                    // 此处获取Qos的各种信息
//                    String propName = "";
//                    double propValue = 0.0;
//                    String propUnit = "";
//                    String propType = "";
//                    for (Iterator<?> iter2 = element.elementIterator(); iter2.hasNext(); ) {
//                        Element element2 = (Element) iter2.next();
//                        System.out.println(element2.getName());
//                        if (element2.getName().equals("qosPropertyName")) {
//                            propName = element2.getText();
//                        } else if (element2.getName().equals("hasValue")) {
//                            propValue = Double.valueOf(element2.getText());
//                        } else if (element2.getName().equals("hasUnit")) {
//                            propUnit = element2.getText();
//                        } else if (element2.getName().equals("hasType")) {
//                            propType = element2.getText();
//                        }
//                    }
//                }
//            }
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }

    }
}
