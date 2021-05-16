import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Scanner;
import org.json.JSONObject;

public class RestApiClient {

	public static void main(String[] args) throws IOException{
		
		if (args.length != 1) {
			System.out.println("Usage: java RestApiClient <server_ip>\n");
			
			return;
		}
		
		String server = args[0];
		Scanner scanner = new Scanner(System.in);
		
		while (true) {
			System.out.println("(Type 'get' or 'set' now.)");
			String getOrSet = scanner.nextLine();
			
			if("get".equalsIgnoreCase(getOrSet)){
				System.out.println("Whose info do you want to get?");
				System.out.println("(Type a person's name now.)");
				String name = scanner.nextLine();
				
				String jsonString = getPersonData(server, name);
				System.out.println(jsonString);
				
			}
			else if("set".equalsIgnoreCase(getOrSet)){
				System.out.println("Whose info do you want to set?");
				System.out.println("(Type a person's name now.)");
				String name = scanner.nextLine();
				
				System.out.println("When was " + name + " born?");
				System.out.println("(Type a year now.)");
				String birthYear = scanner.nextLine();
				
				System.out.println("Can you tell me about " + name + "?");
				System.out.println("(Type a sentence now.)");
				String about = scanner.nextLine();
				
				setPersonData(server, name, birthYear, about);
			} else break;
		}
		scanner.close();	
	}
	
	public static String getPersonData(String server, String name) throws IOException{

		HttpURLConnection connection = (HttpURLConnection) new URL("http://" + server + ":8080/PersonServlet/people/" + name).openConnection();
		
		connection.setRequestMethod("GET");

		int responseCode = connection.getResponseCode();
		if(responseCode == 200){
			String response = "";
			Scanner scanner = new Scanner(connection.getInputStream());
			while(scanner.hasNextLine()){
				response += scanner.nextLine();
				response += "\n";
			}
			scanner.close();

			return response;
		}else{
			System.out.println("?");
		}
		
		// an error happened
		return null;
	}

	public static void setPersonData(String server, String name, String birthYear, String about) throws IOException{
		HttpURLConnection connection = (HttpURLConnection) new URL("http://" + server + ":8080/PersonServlet/people/" + name).openConnection();

		connection.setRequestMethod("POST");
		
		String postData = "name=" + URLEncoder.encode(name);
		postData += "&about=" + URLEncoder.encode(about);
		postData += "&birthYear=" + birthYear;
		
		connection.setDoOutput(true);
		OutputStreamWriter wr = new OutputStreamWriter(connection.getOutputStream());
		wr.write(postData);
		wr.flush();
		
		int responseCode = connection.getResponseCode();
		if(responseCode == 200){
			System.out.println("POST was successful.");
		}
	}
}
