from bs4 import BeautifulSoup


class UniversalParser:
    def parse_with_selectors(
        self, html_content: str, selectors: dict, base_url: str = None
    ) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        product_data = {}

        for field_name, selector in selectors.items():
            if not selector:
                continue

            if field_name == "images":
                product_data[field_name] = self.parse_images(soup, selector, base_url)
            elif field_name == "specifications":
                product_data[field_name] = self.parse_specifications(soup, selector)
            elif field_name == "availability":
                product_data[field_name] = self.parse_availability(soup, selector)
            else:
                product_data[field_name] = self.parse_field(soup, selector)

        return product_data

    def parse_field(self, soup: BeautifulSoup, selector: str) -> str:
        if not selector:
            return ""
        element = soup.select_one(selector)
        if element:
            text = element.get_text().strip()
            return self._normalize_text(text)
        return ""

    def parse_images(
        self, soup: BeautifulSoup, selector: str, base_url: str = None
    ) -> list:
        if not selector:
            return []

        images = []
        img_elements = soup.select(selector)
        for img in img_elements:
            src = img.get("src")
            if src:
                if src.startswith("http"):
                    images.append(src)
                elif base_url:
                    images.append(base_url + src)
                else:
                    images.append(src)
        return images[:3]

    def parse_specifications(self, soup: BeautifulSoup, selector: str) -> dict:
        if not selector:
            return {}

        specs = {}
        spec_elements = soup.select(selector)

        for element in spec_elements:
            parsed = (
                self._try_dt_dd(element)
                or self._try_colon_separated(element)
                or self._try_children_structure(element)
            )

            if parsed:
                key, value = parsed
                # объеденяем
                if key in specs:
                    specs[key] = f"{specs[key]}; {value}"
                else:
                    specs[key] = value
            else:
                text = self._normalize_text(element.get_text().strip())
                if text:
                    if "info" in specs:
                        specs["info"] += "; " + text
                    else:
                        specs["info"] = text

        return specs

    def _try_dt_dd(self, element) -> tuple:
        dt_elem = element.find("dt")
        dd_elem = element.find("dd")
        if dt_elem and dd_elem:
            key = self._normalize_text(dt_elem.get_text().strip())
            value = self._normalize_text(dd_elem.get_text().strip())
            if key and value:
                return key, value
        return None

    def _try_colon_separated(self, element) -> tuple:
        text = self._normalize_text(element.get_text().strip())
        separators = [":", "-"]

        for separator in separators:
            if separator in text:
                parts = text.split(separator, 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        return key, value
        return None

    def _try_children_structure(self, element) -> tuple:
        children = element.find_all(recursive=False)

        if not children:
            return None

        if len(children) == 1:
            return self._try_colon_separated(children[0])

        # многодетка - первый как ключ, остальные как значение
        key = self._normalize_text(children[0].get_text().strip())
        values = []

        for child in children[1:]:
            child_text = self._normalize_text(child.get_text().strip())
            if child_text:
                values.append(child_text)

        if key and values:
            return key, " ".join(values)

        return None

    def _normalize_text(self, text: str) -> str:
        if not text:
            return text

        replacements = {
            "\xa0": " ",  # неразрывный пробел
            "&nbsp;": " ",  # HTML entity
            "\u00a0": " ",  # Unicode пробел
            "\r": " ",  # возврат каретки
            "\t": " ",
            "\n": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = " ".join(text.split())

        return text.strip()

    def parse_availability(self, soup: BeautifulSoup, selector: str) -> str:
        if not selector:
            return "НЕИЗВЕСТНО"

        element = soup.select_one(selector)
        if not element:
            return "НЕИЗВЕСТНО"

        text = element.get_text().strip().lower()

        available_keywords = [
            "в корзину",
            "купить",
            "добавить в корзину",
            "в наличии",
            "есть в наличии",
            "available",
            "in stock",
            "заказать",
            "оформить заказ",
        ]

        not_available_keywords = [
            "нет в наличии",
            "распродано",
            "sold out",
            "out of stock",
            "ожидается",
            "предзаказ",
            "сообщить о поступлении",
        ]

        text_lower = text.lower()

        for keyword in available_keywords:
            if keyword in text_lower:
                return "В наличии"

        for keyword in not_available_keywords:
            if keyword in text_lower:
                return "Нет в наличии"

        return text
