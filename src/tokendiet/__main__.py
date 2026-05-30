"""`tokendiet` / `python -m tokendiet` - 验证安装并跑一个示例。"""
from . import __version__, subtract


def main() -> None:
    print()
    print(f"  tokendiet v{__version__}  ->  安装成功")
    print("  github.com/pornlsy2004-ux/tokendiet   (上下文做减法)")
    print()
    q = "What is the hotel rate cap for Tokyo?"
    ctx = (
        "Economy class is required for flights under 6 hours. "
        "The standard reimbursable hotel rate is capped at $220 per night. "
        "For high-cost cities Tokyo, Zurich and Singapore the cap is $340 per night. "
        "Meals are reimbursed at $75 per day domestic."
    )
    r = subtract(q, ctx)
    print("  demo (lexical backend):")
    print(f"    Q: {q}")
    print(f"    {r.stats['raw_tokens']} tokens  ->  {r.stats['kept_tokens']} tokens")
    print(f"    kept: {r.text}")
    print()
    print("  用法:  from tokendiet import subtract;  subtract(question, context)")
    print()


if __name__ == "__main__":
    main()
