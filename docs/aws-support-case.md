# AWS Support Case — Solicitação de Goodwill Credit
## Amazon Bedrock — Claude Sonnet 4.5 — Agosto 2026

---

**Subject:** Unexpected high cost due to unintended model selection — Requesting goodwill credit

---

**Body:**

Hello AWS Support Team,

I am writing to request a goodwill credit related to unexpected charges from Amazon Bedrock in August 2026.

**Account ID:** 969430605054
**Region:** us-east-1
**Service:** Amazon Bedrock — Claude Sonnet 4.5 (anthropic.claude-sonnet-4-5)
**Charge period:** August 1–25, 2026
**Amount charged:** ~$252.60 (Sonnet 4.5: $229.21 + Bedrock general: $23.39)

---

**What happened:**

I built a WhatsApp AI sales assistant for a small business client using Amazon Bedrock.
During development, the model was set to `anthropic.claude-sonnet-4-5` as a default value
in the configuration file. The original cost estimate in our project documentation
was R$ 10–20/month (~$2–4 USD), based on Claude Sonnet 3 pricing and lower expected volume.

Two factors caused the cost to be ~60x higher than estimated:
1. Claude Sonnet 4.5 pricing is significantly higher than Sonnet 3
2. Actual lead volume (1,200+ conversations/month) exceeded initial estimates

This was an unintentional model selection — we did not consciously choose Sonnet 4.5
for its capabilities over cost. As soon as we identified the issue through AWS Cost Explorer,
we immediately took corrective action.

---

**Corrective actions already taken (August 25, 2026):**

- Replaced model with `anthropic.claude-haiku-3-5` via Lambda environment variable
- Updated default model ID in source code configuration
- Optimized system prompt for the new model
- Projected cost for September: ~$15–20/month (vs ~$490/month with Sonnet 4.5)

---

**Request:**

Given that:
- This was an unintentional configuration error, not deliberate use of a premium model
- We identified and corrected the issue as soon as it was detected
- We are a small business / freelance developer, not a large enterprise
- The corrective action was immediate and permanent

We respectfully request a partial goodwill credit for the August charges related to
Claude Sonnet 4.5 usage ($229.21).

We understand this is not a billing error on AWS's part, and we appreciate any
consideration you can provide.

Thank you for your support.

**Sergio Sena**
SS Technologies
senanetworker@gmail.com
