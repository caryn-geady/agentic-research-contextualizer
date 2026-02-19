from google.adk.models.lite_llm import LiteLlm

def get_model(model_name: str) -> LiteLlm | str:
    
    if 'gemini' in model_name:
        return model_name

    return LiteLlm(model=model_name) # Assume some type of model from litellm