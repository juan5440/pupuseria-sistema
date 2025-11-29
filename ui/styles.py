class Styles:
    # Colors
    PRIMARY = "#3498db"
    SECONDARY = "#2ecc71"
    WARNING = "#f39c12"
    DANGER = "#e74c3c"
    DARK_BG = "#2c3e50"
    LIGHT_BG = "#ecf0f1"
    TEXT_DARK = "#2c3e50"
    TEXT_LIGHT = "#ecf0f1"
    WHITE = "#ffffff"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    HEADER_FONT = ("Segoe UI", 24, "bold")
    SUBHEADER_FONT = ("Segoe UI", 18)
    NORMAL_FONT = ("Segoe UI", 12)
    BOLD_FONT = ("Segoe UI", 12, "bold")
    
    @staticmethod
    def apply_theme(root, dark_mode=False):
        if dark_mode:
            bg = Styles.DARK_BG
            fg = Styles.TEXT_LIGHT
        else:
            bg = Styles.LIGHT_BG
            fg = Styles.TEXT_DARK
            
        root.configure(bg=bg)
        # Add more global styling logic here if needed
