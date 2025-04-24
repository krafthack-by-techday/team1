# helper to generate a colored box with black, bold text
def colored_box(content: str, bg_color: str):
    return f"""
    <div style="
        background-color: {bg_color};
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        color: #000;            /* black text */
        font-weight: bold;      /* bold text */
    ">
    {content}
    </div>
    """
