# Sharing the project with an outside reviewer

_Written 2026-11-06 for sharing with Etter. Web research only. **Not yet tried in our Foundry enrollment.**_

## TL;DR
- **GitHub repo:** easy. Add the reviewer as a collaborator (if the repo is private) and send the link. The README starts with a reviewer path.
- **Live Foundry app:** unsure. We are on the free **AIP Developer Tier**. Palantir **paused new Developer Tier sign-ups on 23 Oct 2026**, so the reviewer probably cannot create an account. Without an account in our enrollment, a Foundry link will not open for them.
- **Recommended:** send the repo + PDFs now, and show the live app on a screen-share. Separately, try the in-product check below (5 minutes) to see whether Foundry offers to add an outside user.

## What we found (sources at the bottom)

| Question | Answer | Confidence |
|---|---|---|
| Can new people sign up for Developer Tier? | No. Online sign-ups paused 23 Oct 2026; existing accounts work as usual | High (Palantir announcement) |
| Can I invite someone into my enrollment? | Not documented for Developer Tier. One guide says Developer Tier has no sharing with other users | Low, unverified |
| If the person **is** a user in my enrollment, how do I give access? | Project-level roles: Owner, Editor, Viewer, Discoverer. Open the project → its **access panel** → add the user or group as **Viewer** | Medium (Foundry docs; exact button label not confirmed in our UI) |
| Can a viewer request access? | Yes. "Request access" sends a role request to the project owner | Medium (docs) |

## 5-minute check in our Foundry (you)
1. Open the project `/kestrel-01f4ab/Medication Safety Signal Monitor`.
2. Open the project's access / sharing panel (top right of the project page).
3. Try to add the reviewer's email as **Viewer**.
   - If Foundry finds or invites them → give **Viewer** on the project only. Then send the Workshop link for **MSSM Safety Officer**.
   - If it only searches existing users and finds nobody → outside sharing is not possible on this tier. Use the fallback.
4. Also check the enrollment's user settings (Control Panel / Settings → Users) for an "invite user" option.

Do **not** give Editor or Owner. Exports are off on every source (D038). Keep them off.

## Fallback (works today)
| Give them | How |
|---|---|
| The code and every write-up | GitHub repo link; README → "Reviewing this project? Start here" |
| What the app looks like | [screens/](../11-handin/screens/README.md) screenshots, [R09 demo guide](../11-handin/reports/pdf/R09-demo-navigation-guide.pdf), [demo deck](../11-handin/deck/MSSM-demo-deck.pdf) |
| The live app | A screen-share call where you drive Foundry |
| A recording | Optional: a 5–10 minute screen recording of the 4 Workshop pages |

## Sources
- [A quick update on AIP Developer Tier (Palantir community, 23 Oct 2026)](https://community.palantir.com/t/a-quick-update-on-aip-developer-tier/7404)
- [Adding users from another organization to a Developer Tier account (community thread)](https://community.palantir.com/t/i-want-to-add-palantir-user-with-different-organization-in-my-developer-tier-account-with-role-based-access-control/6363)
- [Projects and roles (Foundry docs)](https://www.palantir.com/docs/foundry/security/projects-and-roles)
