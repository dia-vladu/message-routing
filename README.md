# message-routing

- The server manages a list of recipients, each recipient being identified by a unique name;
- The client connects to the server and sends a message, specifying the recipient, the issuer, the subject and the text of the message;
- If the recipient appears in the list managed by the server, it will save the message in a local directory with the recipient's name, generating a file name based on the time the message was saved;
- If the recipient does not appear in the list, the server has a list of other servers that it interrogates when receiving a message, in order to determine to which other server the message should be routed;
- The server confirms the acceptance of the message to the client;
- The server can receive messages from other servers on the same connection to check if a certain recipient is in its list;
- If the desired recipient is not found in its list, the server proceeds similarly to the delivery of a message by querying the list of servers to which it can connect directly.
