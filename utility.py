def color_print(r: int, g: int, b: int, text: str) -> None:
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")
