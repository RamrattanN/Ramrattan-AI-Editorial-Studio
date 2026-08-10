import nodemailer from "nodemailer";

export interface EmailProvider {
  sendMagicLink(email: string, link: string): Promise<void>;
}

/**
 * Documented local/development mechanism: writes the magic link to the
 * server log instead of sending real email. This is NOT a fake
 * authenticated user - the Author still must retrieve the real token from
 * the link and complete the real callback exchange; only the transport is
 * a development stand-in, matching the pattern most magic-link libraries
 * ship for local development.
 */
export class ConsoleEmailProvider implements EmailProvider {
  async sendMagicLink(email: string, link: string): Promise<void> {
    console.log(
      `[dev email] Magic link for ${email}: ${link}\n` +
        "Set EMAIL_PROVIDER=smtp and supply SMTP_* to send real email.",
    );
  }
}

/**
 * Production-capable SMTP delivery via nodemailer. Works with any standard
 * SMTP provider (Postmark, SendGrid, Amazon SES, etc.) once SMTP_* is
 * configured; no specific vendor is committed to by this code.
 */
export class SmtpEmailProvider implements EmailProvider {
  private transporter: nodemailer.Transporter;
  private from: string;

  constructor(config: {
    host: string;
    port: number;
    user: string;
    pass: string;
    from: string;
  }) {
    this.transporter = nodemailer.createTransport({
      host: config.host,
      port: config.port,
      secure: config.port === 465,
      auth: { user: config.user, pass: config.pass },
    });
    this.from = config.from;
  }

  async sendMagicLink(email: string, link: string): Promise<void> {
    await this.transporter.sendMail({
      from: this.from,
      to: email,
      subject: "Sign in to Ramrattan AI Editorial Studio",
      text: `Sign in using this link (valid for 15 minutes): ${link}`,
      html: `<p>Sign in using this link (valid for 15 minutes):</p><p><a href="${link}">${link}</a></p>`,
    });
  }
}

export function createEmailProvider(): EmailProvider {
  const kind = process.env.EMAIL_PROVIDER ?? "console";
  if (kind === "smtp") {
    const host = process.env.SMTP_HOST;
    const port = Number(process.env.SMTP_PORT ?? "587");
    const user = process.env.SMTP_USER;
    const pass = process.env.SMTP_PASS;
    const from = process.env.SMTP_FROM;
    if (!host || !user || !pass || !from) {
      throw new Error(
        "EMAIL_PROVIDER=smtp requires SMTP_HOST, SMTP_USER, SMTP_PASS, and SMTP_FROM.",
      );
    }
    return new SmtpEmailProvider({ host, port, user, pass, from });
  }
  return new ConsoleEmailProvider();
}
