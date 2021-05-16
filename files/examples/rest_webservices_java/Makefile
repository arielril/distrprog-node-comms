all:
	@javac Person.java
	@javac DataStore.java
	@javac -cp .:jars/json-20190722.jar:jars/servlet-api.jar PersonServlet.java
	@javac -cp .:jars/json-20190722.jar RestApiClient.java
	
app_install:
	@mkdir jetty/webapps/PersonServlet
	@mkdir jetty/webapps/PersonServlet/WEB-INF
	@mkdir jetty/webapps/PersonServlet/WEB-INF/classes
	@cp web.xml jetty/webapps/PersonServlet/WEB-INF
	@cp *.class jetty/webapps/PersonServlet/WEB-INF/classes
	
rest_webservice:
	@cd jetty && java -jar start.jar && cd ..
		
clean:
	@rm -rf *.class *~ jetty/webapps/PersonServlet
