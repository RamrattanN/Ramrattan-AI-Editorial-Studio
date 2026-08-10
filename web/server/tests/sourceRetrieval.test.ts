import { describe, expect, it } from "vitest";
import { retrieveSource } from "../src/source/retrieve.js";

describe("source retrieval guards", () => {
  it("rejects a malformed URL", async () => {
    const result = await retrieveSource("not a url");
    expect(result.ok).toBe(false);
  });

  it("rejects a non-http(s) scheme", async () => {
    const result = await retrieveSource("ftp://example.com/file.txt");
    expect(result.ok).toBe(false);
  });

  it("rejects localhost", async () => {
    const result = await retrieveSource("http://localhost:4000/internal");
    expect(result.ok).toBe(false);
  });

  it("rejects a loopback IP address", async () => {
    const result = await retrieveSource("http://127.0.0.1:5432/");
    expect(result.ok).toBe(false);
  });

  it("rejects a private RFC1918 address", async () => {
    const result = await retrieveSource("http://192.168.1.10/");
    expect(result.ok).toBe(false);
  });

  it("rejects the cloud-metadata link-local address", async () => {
    const result = await retrieveSource("http://169.254.169.254/latest/meta-data/");
    expect(result.ok).toBe(false);
  });
});
