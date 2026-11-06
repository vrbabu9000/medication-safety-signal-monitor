# Sharing the project with an outside reviewer

_Checked in our Foundry enrollment on 2026-11-06 (v2; v1 was web research only and wrongly guessed sharing was not possible)._

## TL;DR
Invite the reviewer as a user in our enrollment. They get **Viewer** on the project automatically. Then send the Workshop link.

## Facts (seen in Foundry)
| Item | Value |
|---|---|
| Plan | AIP Developer Tier: **5 users** max (1 used today) |
| Invite | Control Panel → Manage user directory → Manage users → **Add new user** (first name, last name, email → *Send invite*). They get an email to create their account |
| Project access | Project panel → 🔒 Access → Roles → Manage: **default role = Viewer for everyone in org `kestrel`**. A new user joins `kestrel`, so they can view the project with no extra step |
| Workshop app link | https://kestrel.usw-16.palantirfoundry.com/workspace/module/view/latest/ri.workshop.main.module.5468606b-d94b-4f0a-b257-a22b207de88d |

## Steps (you)
1. Go to `kestrel.usw-16.palantirfoundry.com/workspace/control-panel/` → **Manage user directory** → **Manage users** → **Add new user**.
2. Enter the reviewer's name and email → **Send invite**.
3. Send the Workshop link once they have accepted the invite.
4. Do **not** make them Editor or Owner. Remove the user after the review (same page).

## Not verified
- Whether a Viewer can see every dataset the Workshop page reads (the default Viewer role covers the whole project, so it should work).
- Whether Palantir's pause on new Developer Tier sign-ups (23 Oct 2026, [announcement](https://community.palantir.com/t/a-quick-update-on-aip-developer-tier/7404)) blocks invites. It is about public sign-ups; invites are a separate flow.
