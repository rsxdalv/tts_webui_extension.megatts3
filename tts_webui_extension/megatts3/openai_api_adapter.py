import os


def _make_tts_fn():
    def tts_fn(
        model: str, text: str, voice: str | None, speed: float | None, params: dict
    ) -> dict:
        from tts_webui_extension.megatts3.tts import tts

        return tts(
            target_text=text,
            reference_audio_path=params.get("reference_audio_path", ""),
            latent_npy_path=params.get("latent_npy_path", ""),
            inference_steps=params.get("inference_steps", 32),
            intelligibility_weight=params.get("intelligibility_weight", 0.8),
            similarity_weight=params.get("similarity_weight", 0.8),
        )

    return tts_fn


def register():
    try:
        if os.environ.get("OPENAI_PROXY_HOST"):
            register_unsafe_outprocess()
        else:
            register_unsafe_inprocess()
    except Exception as e:
        print(f"Error registering MegaTTS3 API adapter: {e}")
        print("MegaTTS3 TTS will not be available on the OpenAI API.")


def register_unsafe_inprocess():
    from tts_webui_extension.openai_tts_api.services.tts_adapter_registry import (
        register_tts_adapter,
    )

    register_tts_adapter("megatts3", _make_tts_fn())


def register_unsafe_outprocess():
    from tts_webui_extension.openai_tts_api.harness import setup_oai_server

    setup_oai_server(
        tts_fn=_make_tts_fn(),
        get_voices_fn=lambda model: [],
        model="megatts3",
    )

