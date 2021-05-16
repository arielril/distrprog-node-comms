import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class PersonServlet extends HttpServlet {

	@Override
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
		
		String requestUrl = request.getRequestURI();
		String name = requestUrl.substring("/people/".length());
		String last = requestUrl.substring(requestUrl.lastIndexOf('/')).substring(1);
		
		System.out.println("requesting " + last + "\n");
		
		Person person = DataStore.getInstance().getPerson(last);
		
		if (person != null){
			String json = "{\n";
			json += "\"name\": \"" + person.getName() + "\",\n";
			json += "\"about\": \"" + person.getAbout() + "\",\n";
			json += "\"birthYear\": " + person.getBirthYear() + "\n";
			json += "}";
			response.getOutputStream().println(json);
		}else{
			//That person wasn't found, so return an empty JSON object. We could also return an error.
			response.getOutputStream().println("{}");
		}
	}

	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {

		String name = request.getParameter("name");
		String about = request.getParameter("about");
		int birthYear = Integer.parseInt(request.getParameter("birthYear"));
		
		DataStore.getInstance().putPerson(new Person(name, about, birthYear));
	}
}
