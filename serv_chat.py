#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor


MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        #A COMPLETAR
        users = ""
        for user in self.factory.users:
            users+=user
            users+=" "

        users = users[0:(len(users)-1)]
        if len(users) == MAX_USERS:
            connectionLost(self, 1)
        else:
            self.sendLine( "FTR0 0 0 0".encode( "utf-8" ) )
            self.sendLine( ("USR{}".format( users)).encode( "utf-8" ) )

        
    def connectionLost(self, reason):
        userLost = self.name
        self.factory.users.pop(self.name, None)
        for i in self.factory.users:
            user = self.factory.users[i]
            user.sendLine(("OUT{}".format(userLost)).encode("utf-8"))
        #A COMPLETAR
    def lineReceived(self, line):
        mensage = line.decode("utf-8")

        if mensage.startswith("NME"):
            userName = mensage[3:]
            #Si tienes caracteres prohibidos
            if " " in userName:
                self.sendLine( ("-{}".format( 2 )).encode( "utf-8" ) )
            #Si el nombre es demasiado largo
            elif len(userName) > MAX_USER_LENGTH:
                self.sendLine( ("-{}".format( 3 )).encode( "utf-8" ) )

            #Si el nombre ya existe
            elif userName in self.factory.users:
                self.sendLine( ("-{}".format( 4 )).encode( "utf-8" ) )

            else:
                #Enviar a todos los usuarios que ha entrado un usuario nuevo
                for i in self.factory.users:
                    self.factory.users[i].sendLine(("INN{}".format(userName)).encode("utf-8"))
                self.factory.users[userName] = self
                self.name = userName
                self.sendLine("+".encode( "utf-8"))

        elif mensage.startswith("MSG"):
            mensage = mensage[3:]
            #Si el mensaje es demasiado largo
            if len(mensage) > MAX_MSG_LENGTH:
                self.sendLine( ("-{}".format( 5 )).encode( "utf-8" ) )
            else:
                self.sendLine("+".encode( "utf-8"))
                for i in self.factory.users:
                    if self.name not in self.factory.users[i].name:
                        self.factory.users[i].sendLine(("MSG{}{}".format(self.name,mensage)).encode("utf-8"))
        else:
            self.sendLine( ("-{}".format( 0 )).encode( "utf-8" ) )

                


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
         
        return ChatProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(PORT, ChatFactory())
    reactor.run()
