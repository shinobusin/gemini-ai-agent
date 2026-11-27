import json
import urllib.request


def convert_currency(amount: float, from_currency: str, to_currency: str = "INR") -> str:
    """Converts an amount from one currency (e.g., USD, EUR, GBP) to another (default INR) using live rates."""
    try:
        src = from_currency.strip().upper()
        dst = to_currency.strip().upper()
        if src == dst:
            return f"{amount:.2f} {src} = {amount:.2f} {dst}"

        url = f"https://api.frankfurter.app/latest?amount={amount}&from={src}&to={dst}"
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read().decode())

        converted = data["rates"][dst]
        return f"{amount:.2f} {src} = {converted:.2f} {dst} (Rate date: {data['date']})"
    except Exception as e:
        return f"Currency conversion failed: {e}"