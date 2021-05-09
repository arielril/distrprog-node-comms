import java.rmi.RemoteException;

public interface INode {
  public void isAlive() throws RemoteException;

  public void downloadResource(String resourceId) throws RemoteException;
}
