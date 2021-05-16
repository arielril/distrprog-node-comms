import java.util.HashMap;
import java.util.Map;

public class DataStore {
	private Map<String, Person> personMap = new HashMap<>();
	private static DataStore instance = new DataStore();
	
	public static DataStore getInstance(){
		return instance;
	}

	private DataStore(){
		personMap.put("Bill", new Person("Bill", "William is his real name.", 1955));
		personMap.put("Amanda", new Person("Amanda", "Amanda is a biker.", 1986));
		personMap.put("Stanley", new Person("Stanley", "Stanley is Amanda's dog.", 2015));
	}

	public Person getPerson(String name) {
		return personMap.get(name);
	}

	public void putPerson(Person person) {
		personMap.put(person.getName(), person);
	}
}
