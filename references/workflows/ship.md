# Ship

1. Select the active plan explicitly and load the review workflow. Re-run applicable checks; inspect fresh evidence for every criterion on this plan.
2. Automated criteria require current successful results. Manual criteria require the user's explicit confirmation, recorded accurately; do not infer approval from silence or unrelated prior messages.
3. Any unmet or unverified criterion means not shippable. Report the missing evidence and stop.
4. When all criteria pass, mark only the selected plan shipped and record an activity_log entry in the same transaction.
5. Report delivered behavior, evidence, deployment steps/costs where relevant, and post-deployment checks. Shipped is Atelier's verified-contract state; it does not imply deployment. Deploy, publish, commit or push only when the user separately authorized that action.
