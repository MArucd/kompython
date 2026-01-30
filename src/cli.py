import asyncio
import sys

from factory import ParserFactory


async def test_full_pipeline(url):
    use_case = await ParserFactory.create_parse_product_use_case()

    try:
        product_data = await use_case.execute(url)

        print("\nРезультат парсинга:")
        for key, value in product_data.items():
            print(f"\n{key}: {value}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    url = sys.argv[1]
    asyncio.run(test_full_pipeline(url))
