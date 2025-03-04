from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def get_image_url(text: str) -> str:
    """
    Busca uma imagem relacionada ao texto usando DuckDuckGo e retorna a URL
    """
    try:
        search = DuckDuckGoSearchAPIWrapper(safesearch="off", source="images")
        results = search.results(text, 1)[0]['image']        
        return results

    except Exception as e:
        print(f"Erro ao buscar imagem: {e}")
        return "Ocorreu um erro ao buscar a imagem."