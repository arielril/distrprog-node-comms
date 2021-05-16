
public interface ISupernode {
  // TODO define what is the resource
  public int register(Strings nodeId, Class resources);

  // send the Multicast IP request
  public void searchResources(String[] hashId);

  public void getResult(Result r);
}
