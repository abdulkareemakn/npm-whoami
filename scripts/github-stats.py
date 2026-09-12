"""Run with python3 scripts/github-stats.py; uses the existing gh login."""

import json
import subprocess
import sys


def query_pages(query, **variables):
    args = ["gh", "api", "graphql", "--paginate", "--slurp", "-f", f"query={query}"]
    for key, value in variables.items():
        args.extend(["-f", f"{key}={value}"])
    pages = json.loads(subprocess.check_output(args, text=True))
    for page in pages:
        if page.get("errors"):
            raise RuntimeError(page["errors"])
    return [page["data"] for page in pages]


def count_commits(nodes, user_id):
    mine = [node for node in nodes if node["author"]["user"] == {"id": user_id}]
    return len(mine), sum(n["additions"] for n in mine), sum(n["deletions"] for n in mine)


def main():
    username = "abdulkareemakn"
    pages = query_pages("""
      query($login: String!, $endCursor: String) {
        user(login: $login) {
          id
          repositories(first: 100, after: $endCursor,
            ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
            totalCount
            nodes { nameWithOwner }
            pageInfo { hasNextPage endCursor }
          }
        }
      }
    """, login=username)
    user_id = pages[0]["user"]["id"]
    repos = [repo for page in pages for repo in page["user"]["repositories"]["nodes"]]
    assert len(repos) == pages[0]["user"]["repositories"]["totalCount"]
    commits = additions = deletions = authored_repos = 0
    for index, repo in enumerate(repos, 1):
        owner, name = repo["nameWithOwner"].split("/")
        pages = query_pages("""
          query($owner: String!, $name: String!, $author: ID!, $endCursor: String) {
            repository(owner: $owner, name: $name) {
              defaultBranchRef { target { ... on Commit {
                history(first: 100, after: $endCursor, author: {id: $author}) {
                  totalCount
                  nodes { author { user { id } } additions deletions }
                  pageInfo { hasNextPage endCursor }
                }
              } } }
            }
          }
        """, owner=owner, name=name, author=user_id)
        nodes = []
        for page in pages:
            branch = page["repository"]["defaultBranchRef"]
            if branch:
                history = branch["target"]["history"]
                nodes.extend(history["nodes"])
        if nodes:
            assert len(nodes) == history["totalCount"]
        count, added, deleted = count_commits(nodes, user_id)
        commits += count
        additions += added
        deletions += deleted
        authored_repos += count > 0
        print(f"Processed {index}/{len(repos)} repositories", file=sys.stderr, flush=True)
    # ponytail: matches the original per-repository totals; deduplicate commit IDs if forks should count once.
    print(json.dumps(dict(contributed=len(repos), repositories_with_authored_commits=authored_repos,
                          commits=commits, additions=additions, deletions=deletions,
                          net_lines=additions - deletions), indent=2))


if __name__ == "__main__":
    assert count_commits([
        {"author": {"user": {"id": "me"}}, "additions": 10, "deletions": 3},
        {"author": {"user": None}, "additions": 99, "deletions": 99},
    ], "me") == (1, 10, 3)
    main()
