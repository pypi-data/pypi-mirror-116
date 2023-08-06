import networkx as nx


class TransformDAG:
    __root__ = "<ROOT>"

    def __init__(self, initial_columns):
        self.DAG = nx.DiGraph()
        self.leafs = set()

        for column in initial_columns:
            self.DAG.add_node(f"RAW--{column}", element=None)
            self.DAG.add_edge(self.__root__, f"RAW--{column}")

    def add(self, transformation):
        self.DAG.add_node(transformation.name, element=transformation)
        self.leafs.add(transformation.name)

        columns = [dep if dep != transformation.name else f"RAW--{dep}" for dep in transformation.input_columns]
        for dependency in columns:
            if dependency not in self.DAG and f"RAW--{dependency}" in self.DAG:
                dependency = f"RAW--{dependency}"

            self.DAG.add_edge(dependency, transformation.name)

        # Attach directly to root if no dependencies are present
        if not columns:
            self.DAG.add_edge(self.__root__, transformation.name)

    def __iter__(self):
        stages = {}
        for leaf in self.leafs:
            try:
                all_paths = list(nx.all_simple_paths(self.DAG, self.__root__, leaf))
            except:
                raise ValueError(f"Could not match dependencies for {leaf}")

            for path in all_paths:
                for idx, (prev, job) in enumerate(zip(path, path[1:])):
                    if self.DAG.nodes[job]["element"] is not None:
                        job_idx = max(stages.get(prev, 0) + 1, idx)
                        if job not in stages:
                            stages[job] = job_idx
                        else:
                            stages[job] = max(job_idx, stages[job])

        for job, idx in sorted(stages.items(), key=lambda x: x[1]):
            yield self.DAG.nodes[job]["element"]
