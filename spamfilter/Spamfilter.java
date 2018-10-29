import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.Scanner;

/*
Special thanks to Teemu Roos from the University of Helsinki and his course DATA15001 Introduction to Artificial Intelligence for the template to this code! Spam and ham word count files are originally from the Apache SpamAssassin project.
*/

public class Spamfilter {

    private final static String SPAM_PATH = "spamcount.txt";
    private final static String HAM_PATH = "hamcount.txt";

    private static List<List<String>> readMessage(String input) throws IOException {
        //String teksti = new String(Files.readAllBytes(Paths.get(file)));
        List<String> list = Arrays.asList(input.split("\\."));
        List<List<String>> listlist = new ArrayList<>();
        for (String sentence : list) {
            listlist.add(Arrays.asList(sentence.split("\\s+")));
        }
        return listlist;
    }

    private static Map<String, Integer> readOccurences(String file)
            throws FileNotFoundException {
        Map<String, Integer> counts;
        try (Scanner lukija = new Scanner(new File(file))) {
            counts = new HashMap<>();
            while (lukija.hasNext()) {
                int occurences = lukija.nextInt();
                String word = lukija.next();
                counts.put(word, occurences);
            }
        }

        return counts;
    }
    
    private static void evaluate(List<String> email, Map<String, Integer> spam, Map<String, Integer> ham, double spamNo, double hamNo, int ordinal, double[] results) throws Exception {
        
        double logR = 0;

        for (String word : email) {
            double spamprob = 0.00001;
            double hamprob  = 0.00001;
            if (spam.containsKey(word)) {
                if (spam.get(word) != 0) spamprob = spam.get(word) / spamNo;   
            }
            if (ham.containsKey(word)) {
                if (ham.get(word) != 0) hamprob = ham.get(word) / hamNo;    
            }

            logR += Math.log(spamprob) - Math.log(hamprob);
        }

        double r = Math.exp(logR);

        results[ordinal] = (r / (1 + r));
    }

    private static String printSentence(List<String> sentence) {
	String output = "\"";
	for (String word : sentence) {
		output += word + " ";
	}
	output += "\"";
	return output;
    }

    public static void main(String[] args) throws Exception {
        Map<String, Integer> spam = readOccurences(SPAM_PATH);
        Map<String, Integer> ham = readOccurences(HAM_PATH);
        double spamNo = spam.values().stream().mapToInt(Number::intValue).sum();
        double hamNo = ham.values().stream().mapToInt(Number::intValue).sum();
	Scanner reader = new Scanner(System.in);
	String filePath = reader.nextLine();
        List<List<String>> email = readMessage(filePath);
	double[] results = new double[email.size()];
        for (int i = 0; i < email.size(); i++) {
            evaluate(email.get(i), spam, ham, spamNo, hamNo, i, results);
        }
	int spam50 = 0;
	for (int i = 0; i < results.length; i++) {
		System.out.println("Sentence " + printSentence(email.get(i)) + " has a " + Math.round(results[i] * 100) + " % probability of being spam.");
		if (results[i] >= 0.5) spam50++; 
	}
	System.out.println(Math.round(100 * ((double) spam50 / email.size())) + " % of sentences in chosen data set are classified as spam by us.");
    }

}
