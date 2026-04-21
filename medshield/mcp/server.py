import asyncio
from mcp.server.fastmcp import FastMCP
from medshield import Sanitizer

# Create an MCP server instance
mcp = FastMCP("MedShield Privacy Server")

# Shared global sanitizer instance
# By default, we'll use MASK to ensure determinism across tools
sanitizer = Sanitizer(options={"level": "MASK", "preserveMedicalContext": True})


@mcp.tool()
async def sanitize_text(text: str, level: str = "MASK") -> str:
    """
    Sanitize PII/PHI from the provided text.

    Args:
        text: The raw text containing sensitive medical information.
        level: The severity of sanitization ('MASK', 'SYNTHESIZE', or 'REDACT'). Defaults to MASK.
    """
    # Create a temporary tool-specific option if it differs, but using shared Vault
    # For simplicity, we temporarily update the option, run, and restore,
    # but practically we can just configure a new instance sharing the same vault.

    # We will instantiate a localized engine but share the vault for context.
    local_sanitizer = Sanitizer(
        options={"level": level, "preserveMedicalContext": True}
    )
    local_sanitizer.vault = sanitizer.vault

    return local_sanitizer.sanitize(text)


@mcp.tool()
async def reset_privacy_context() -> str:
    """
    Resets the deterministic Token Vault.
    Call this when starting a new patient session so that [PERSON_0] restarts.
    """
    sanitizer.reset_context()
    return "Privacy context reset successfully. Ready for new session."


def main():
    """Entry point for the MCP server binary."""
    mcp.run()


if __name__ == "__main__":
    main()
