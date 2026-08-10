import { isIP } from "node:net";
import { lookup } from "node:dns/promises";
import { convert as htmlToText } from "html-to-text";

const FETCH_TIMEOUT_MS = 10_000;
const MAX_BYTES = 2_000_000; // 2 MB - enough for an article page, bounded.
const MAX_SUMMARY_CHARS = 12_000; // bounded input to the OpenAI task.

export type RetrievalResult =
  | { ok: true; text: string }
  | { ok: false; error: string };

/**
 * Blocks fetches to loopback, link-local, private (RFC1918), and
 * cloud-metadata addresses. This is a minimal, explicit SSRF guard - not a
 * full network-policy solution - matching the "safe, minimal retrieval
 * implementation" scope of Web Walking Skeleton 01, item 5.
 */
function isBlockedAddress(address: string): boolean {
  const version = isIP(address);
  if (version === 4) {
    const octets = address.split(".").map(Number);
    const [a, b] = octets;
    if (a === 127) return true; // loopback
    if (a === 10) return true; // RFC1918
    if (a === 169 && b === 254) return true; // link-local / cloud metadata
    if (a === 172 && b >= 16 && b <= 31) return true; // RFC1918
    if (a === 192 && b === 168) return true; // RFC1918
    if (a === 0) return true;
    return false;
  }
  if (version === 6) {
    const normalized = address.toLowerCase();
    if (normalized === "::1") return true; // loopback
    if (normalized.startsWith("fe80:")) return true; // link-local
    if (normalized.startsWith("fc") || normalized.startsWith("fd")) return true; // unique local
    return false;
  }
  return true; // could not classify - fail closed.
}

async function assertSafeUrl(url: URL): Promise<void> {
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new Error("Only http:// and https:// URLs are supported.");
  }
  if (url.hostname === "localhost") {
    throw new Error("Requests to localhost are not permitted.");
  }

  let addresses: string[];
  try {
    const results = await lookup(url.hostname, { all: true });
    addresses = results.map((r) => r.address);
  } catch {
    throw new Error("The source URL's host could not be resolved.");
  }

  if (addresses.length === 0 || addresses.some(isBlockedAddress)) {
    throw new Error("This source URL points to a disallowed network address.");
  }
}

/**
 * Retrieves a URL's textual content for the Editorial Direction task.
 * Fails closed with a plain error rather than fabricating content when
 * retrieval is not possible - never solves paywalls or browser automation
 * in this slice.
 */
export async function retrieveSource(rawUrl: string): Promise<RetrievalResult> {
  let url: URL;
  try {
    url = new URL(rawUrl);
  } catch {
    return { ok: false, error: "That does not look like a valid URL." };
  }

  try {
    await assertSafeUrl(url);
  } catch (error) {
    return { ok: false, error: (error as Error).message };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      redirect: "follow",
      headers: {
        "User-Agent": "RamrattanEditorialStudio/0.1 (+walking-skeleton-01)",
        Accept: "text/html,application/xhtml+xml",
      },
    });

    if (!response.ok) {
      return {
        ok: false,
        error: `The source could not be retrieved (HTTP ${response.status}).`,
      };
    }

    const contentType = response.headers.get("content-type") ?? "";
    if (!contentType.includes("html") && !contentType.includes("text")) {
      return {
        ok: false,
        error: "This source's content type is not supported yet.",
      };
    }

    const reader = response.body?.getReader();
    if (!reader) {
      return { ok: false, error: "The source returned no content." };
    }

    let received = 0;
    const chunks: Uint8Array[] = [];
    // Bound how much of the body we read to avoid unbounded memory use.
    while (received < MAX_BYTES) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) {
        chunks.push(value);
        received += value.byteLength;
      }
    }
    await reader.cancel().catch(() => undefined);

    const html = Buffer.concat(chunks.map((c) => Buffer.from(c))).toString("utf-8");
    const text = htmlToText(html, {
      wordwrap: false,
      selectors: [
        { selector: "script", format: "skip" },
        { selector: "style", format: "skip" },
        { selector: "nav", format: "skip" },
        { selector: "footer", format: "skip" },
        { selector: "img", format: "skip" },
        { selector: "a", options: { ignoreHref: true } },
      ],
    })
      .replace(/\n{3,}/g, "\n\n")
      .trim();

    if (text.length < 200) {
      return {
        ok: false,
        error:
          "Not enough readable content was found at this URL. It may require a browser, a login, or be paywalled.",
      };
    }

    return { ok: true, text: text.slice(0, MAX_SUMMARY_CHARS) };
  } catch (error) {
    if ((error as Error).name === "AbortError") {
      return { ok: false, error: "The source took too long to respond." };
    }
    return { ok: false, error: "The source could not be retrieved." };
  } finally {
    clearTimeout(timeout);
  }
}
