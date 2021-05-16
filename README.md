# Distributed Programming - Node Communications

Distributed Programming - Node Communications

## Notes

### Super Nodes
- Communicate over Multi-cast with other Super nodes
- Have a list of nodes with a reference for the resources of each node
- Receive node request for resource searching
- Check with the other super nodes if they have the resource (**multi-casting**)
- Receive alive requests from registered nodes, if the node doesn't send a request -> remove it

### Nodes
- Register to a super node (cli opt)
- Have a list of resources - scan a folder and create a hash for each resource
- Timely send alive requests to super nodes (5s)
- Have an endpoint to "download" a resource list (one or many)

## Resources

- https://github.com/miguelgrinberg/microblog/tree/master
