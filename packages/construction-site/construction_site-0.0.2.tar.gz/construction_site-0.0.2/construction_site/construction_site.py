from rdflib import Graph, Namespace, URIRef
from rdflib.graph import ConjunctiveGraph, ReadOnlyGraphAggregate
from pyshacl import validate
from pathlib import Path

from .parse_functions import parse_json

CS_NS = Namespace("urn:graphs:")


class ConstructionSite:
    def __init__(self, **kwargs) -> None:
        if "namespace" in kwargs and isinstance(kwargs.namespace, Namespace):
            self.ns = kwargs.namespace
        else:
            self.ns = Namespace("http://localhost/")

        self.g = ConjunctiveGraph()
        self.prefix("files", CS_NS)
        self.prefix("source", self.ns)

    def _add_to_graph(self, triples_gen, context):
        for s, p, o in triples_gen:
            self.g.add((s, p, o, context))

    def prefix(self, prefix, namespace):
        if isinstance(namespace, Namespace):
            self.g.namespace_manager.bind(prefix, namespace)
        else:
            self.g.namespace_manager.bind(prefix, Namespace(namespace))
        return self

    def load_json(self, json, name=None):
        if Path(json).is_file():
            with open(json, "r") as f:
                triples_gen = parse_json(f, self.ns)

                if name is not None:
                    context = CS_NS[name]
                else:
                    context = CS_NS[f.name]
        else:
            if name is not None:
                context = CS_NS[name]
            else:
                raise Exception("A JSON string was given, but no name was supplied")

        self._add_to_graph(triples_gen, context)
        return self

    def construct(self, query, name):
        context = URIRef(CS_NS[name])
        try:
            with open(query, "r") as f:
                q = f.read()
                qres = self.g.query(q)
        except FileNotFoundError:
            qres = self.g.query(query)

        self._add_to_graph(qres, context)
        return self

    def serialize(self, g):
        return self.g.serialize(format="turtle").decode("utf-8")

    def validate(self, shacl):
        sg = Graph()
        sg.parse(shacl)

        r = validate(
            g,
            shacl_graph=sg,
            ont_graph=None,
            inference="rdfs",
            abort_on_error=False,
            meta_shacl=False,
            advanced=False,
            js=False,
            debug=False,
        )
        conforms, results_graph, results_text = r
        print(results_text)
        return conforms

    def collect(self):

        return self

    def run():
        return ReadOnlyGraphAggregate()
