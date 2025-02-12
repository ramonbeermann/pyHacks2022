# -*- coding: utf-8 -*-
import sys

# Nur unter Linux: epoll statt select verwenden,
# um bei sehr vielen offenen Verbindungen performanter zu sein.
if sys.platform.startswith('linux'):
    from twisted.internet import epollreactor
    epollreactor.install()

from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.http2 import H2Factory

# Optional: GZip-Kompression
# from twisted.web.encoding import GzipEncoderFactory

class SimpleResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        # Beispiel-Antwort
        return b"<html><center><h1>I'm a faster Twisted server!!</h1></center></html>"

# Root-Resource definieren und Child-Ressource anbinden
root = resource.Resource()
root.putChild(b"simple", SimpleResource())

# Normales Site-Objekt erzeugen ...
site = server.Site(root)

# ... und HTTP/2 aktivieren
h2_factory = H2Factory(site)

# Optional: GZip einschalten, wenn sinnvoll
# gzip_factory = GzipEncoderFactory(h2_factory)
# reactor.listenTCP(8080, gzip_factory)

# Ohne GZip, nur HTTP/2:
reactor.listenTCP(8080, h2_factory)

# Hinweis: Möchte man HTTPS + HTTP/2 (h2 over TLS):
# from twisted.internet.ssl import CertificateOptions
# ssl_context = CertificateOptions(
#     # Zertifikats-Parameter angeben, z.B. certKeyPair usw.
# )
# reactor.listenSSL(8443, h2_factory, ssl_context)

# Server starten
reactor.run()
