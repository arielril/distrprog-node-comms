package calc;

import javax.xml.namespace.QName;
import javax.xml.ws.Service;
import java.net.URL;

class CalculadoraClient {
	public static void main(String args[]) throws Exception {
		URL url = new URL("http://127.0.0.1:9876/calc?wsdl");
		QName qname = new QName("http://calc/","CalculadoraServerImplService");
		Service ws = Service.create(url, qname);
		CalculadoraServer calc = ws.getPort(CalculadoraServer.class);

		System.out.println("Soma (5+2): " + calc.soma(5,2));
		System.out.println("Subtracao (5-2): " + calc.subtracao(5,2));
		System.out.println("Multiplicacao (5*2): " + calc.multiplicacao(5,2));
		System.out.println("Divisao (5/2): " + calc.divisao(5,2));
	}
}