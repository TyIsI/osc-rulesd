# osc-rulesd

OSC Rules Daemon

Description
-----------

This project provides a locally hosted "brain" to OSC implementations.

It does so by providing a daemon that matches messages to its configured rules and sends out control messages accordingly.

Configuration
-------------

Specify the clients in the destination section and use those names in the push sections of the rules.
You can specify multiple push destinations per matching rule.