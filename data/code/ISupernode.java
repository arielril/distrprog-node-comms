import java.rmi.RemoteException;
import java.rmi.server.ServerNotActiveException;

public interface ISupernode {
  // TODO define what is the resource
  public int register(Class<?> resources) throws RemoteException, ServerNotActiveException;

  public void searchResource(String hashId) throws RemoteException;

  public void getResult(Result r) throws RemoteException;
}
