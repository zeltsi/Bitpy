# Bitpy

This code is our attempt at implementing some of the core functions in Bitcoin. Currently this code allows the user to send and receive version messages, ping, pongs, verack, and getblock. We're currently working on implementing a bloom filters which will allow users to ask the remote node for more specific information (filter by address and transaction id).

We might add some more features in the future.

The code is in Python 3.5. The GUI was built using pyqt.

In order to run this code you might need to install the following packages:

- hashlib
- pyqt
- ecdsa
- base58
- netaddr

This code was created by Shlomi Zeltsinger and Alexis gallepe. you can read more about our working process at http://zeltsinger.com

- This code is for educational purposes only. Don’t use with any sensitive devices or as a real live Bitcoin client.
