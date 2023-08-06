from __future__ import annotations

from typing import Any, Iterable, Literal, Sequence

import attr
import networkx as nx


__all__ = ["PoSet", "Pair", "Chain", "CMP"]


Pair = tuple[Any, Any]
Chain = Sequence[Any]
CMP = Literal["<", ">", "||", "="]


@attr.frozen
class PoSet:
   """Hasse diagram representation of partially ordered set.
   """
   hasse: nx.DiGraph = attr.ib(factory=nx.DiGraph)

   def __len__(self) -> int:
       return len(self.hasse)

   def __iter__(self) -> Iterable[Any]:
       yield from self.hasse.nodes

   def compare(self, left: Any, right: Any) -> CMP:
       if left == right:
           return "="
       elif nx.has_path(self.hasse, left, right):
           return "<"
       elif nx.has_path(self.hasse, right, left):
           return ">"
       return "||"

   def __contains__(self, elem: Any) -> bool:
       return elem in self.hasse.nodes

   def add(self, chain: Chain) -> PoSet:
       hasse = nx.DiGraph(self.hasse)
       nx.add_path(hasse, chain)
       return attr.evolve(self, hasse=nx.transitive_reduction(hasse))

   @staticmethod
   def from_chains(*chains: list[Chain]) -> PoSet:
       hasse = nx.DiGraph()
       for chain in chains:
           nx.add_path(hasse, chain)
       return PoSet(nx.transitive_reduction(hasse))
