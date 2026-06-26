from ddgs import DDGS


def search_web(query, max_results=5):

    try:

        results_text = ""

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )

        print("\nRAW DDGS RESULTS:")
        print(results)

        for i, result in enumerate(results, start=1):

            title = result.get("title", "")
            body = result.get("body", "")
            href = result.get("href", "")

            results_text += (
                f"Result {i}\n"
                f"Title: {title}\n"
                f"Content: {body}\n"
                f"Source: {href}\n\n"
            )

        return results_text

    except Exception as e:

        print(f"\nWEB SEARCH ERROR: {e}\n")

        return ""