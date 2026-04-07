from src.llm_extractor import run_llm_extraction_for_review


def main():
    result = run_llm_extraction_for_review(
        "test_1",
        "The staff were amazing but service was slow and disorganized"
    )

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()