# Harborline Platform Operations Handbook

Fictional evaluation document; it describes no real organization, person, or product.

Version 3.2. This handbook applies to every production service operated by Harborline engineering teams. Where a service runbook conflicts with this handbook, this handbook takes precedence unless the runbook has been approved as an exception by the reliability council.

## 1. Purpose and Scope

This handbook defines how Harborline engineering teams operate production services: who is on call, how incidents are classified and communicated, how changes are approved, how data is protected, and how services are retired. It does not cover internal tooling that has no customer impact, which is governed by the internal tools guide. Teams that operate a service with fewer than 50 customers may follow the lightweight process in Appendix A instead of sections 7 and 10, but every other section still applies to them. The handbook is reviewed every 12 months by the reliability council, and proposals for changes may be submitted at any time through the reliability council's request form.

## 2. Roles and Responsibilities

Every production service has a named service owner, who is accountable for its availability, cost, and documentation. During an incident, three roles are assigned. The incident commander coordinates the response and makes the final call on mitigation steps. The communications lead writes every customer-facing update and keeps the status page current. The scribe records the timeline in the incident channel so that the postmortem can be written from first-hand notes. One person may hold more than one role in a SEV-3 or SEV-4 incident, but in a SEV-1 or SEV-2 incident the incident commander must not also act as communications lead. The service owner is not automatically the incident commander; the on-call primary takes that role until they hand it over explicitly in the incident channel.

## 3. On-call Rotation

Each team runs a weekly rotation with a primary and a secondary engineer. The handover happens every Monday at 10:00 local time and must include a written summary of open incidents and pending changes. The primary must acknowledge a page within 5 minutes. If the primary has not acknowledged within 10 minutes, the page is sent to the secondary automatically. If neither engineer has acknowledged within 20 minutes, the page is sent to the team's engineering manager. Engineers may swap shifts with each other, but a swap must be recorded in the scheduling tool at least 24 hours before the shift begins. Nobody may be primary for more than two consecutive weeks.

## 4. Incident Severity Levels

SEV-1 means a full outage of a customer-facing service or a credible risk of customer data loss. SEV-2 means a major degradation that affects more than 10 percent of customers, or any degradation of the billing system. SEV-3 means a minor degradation for which a workaround exists. SEV-4 means a cosmetic problem or a defect with no customer impact. The incident commander sets the initial severity and may raise or lower it at any time; each change must be announced in the incident channel with the reason. If there is doubt between two levels, the higher level is chosen.

## 5. Customer Communication

For a SEV-1 incident, the first status page update must be published within 15 minutes of the incident being declared, and further updates follow at least every 30 minutes until the incident is resolved. For a SEV-2 incident declared during business hours, the first update must be published within 60 minutes of declaration. Business hours are Monday to Friday, 08:00 to 19:00 local time. For a SEV-2 incident declared outside business hours, the first update must be published by 09:00 on the next business day, unless the incident is escalated to SEV-1 in the meantime, in which case the SEV-1 rule applies from the moment of escalation. SEV-3 and SEV-4 incidents are not posted on the status page; they are summarized in the next release notes instead.

## 6. Escalation

If an incident is not mitigated within 2 hours, the incident commander must inform the engineering director. If a SEV-1 incident is not mitigated within 4 hours, the engineering director must inform the vice president of engineering and the head of customer support. Escalation to another team is requested through that team's on-call page, never through direct messages. When an incident involves customer personal data, the incident commander must also notify the privacy office within 24 hours of the incident being declared, regardless of severity.

## 7. Change Management and Freeze Windows

Standard changes, which follow a pre-approved template, may be deployed at any time outside a freeze window. Normal changes must be approved by the change advisory board, which meets every Tuesday. A change freeze applies during the last 5 business days of each calendar quarter and from December 20 to January 3. During a freeze only emergency changes are allowed. An emergency change during a freeze requires approval from the vice president of engineering, and a post-incident review of the change must be completed within 5 business days of the deployment. Emergency changes outside a freeze window need approval only from the on-call incident commander.

## 8. Backup and Restore

Production databases are snapshotted daily, and daily snapshots are retained for 35 days. Weekly snapshots are retained for 12 weeks, and monthly snapshots for 13 months. Every service must perform a restore test once per quarter and record the result in the reliability tracker. A restore request is tracked as a restore ticket. A restore ticket may be closed only after the service owner has verified the checksums of the restored data and has run read validation against it for at least 24 hours. If the restore was performed because of an incident, the restore ticket must also be linked to the postmortem.

## 9. Postmortems

A postmortem is required for every SEV-1 and SEV-2 incident and is optional for SEV-3. The postmortem draft must be published within 5 business days of the incident being resolved, and it is reviewed at the weekly reliability review. Postmortems are blameless: they describe systems and decisions, not individual fault. Each postmortem lists action items with an owner, and every action item must be completed within 30 days of the review unless the reliability council grants an extension.

## 10. Capacity Planning

Each service publishes a capacity forecast every quarter. A compute expansion must be requested when sustained CPU utilization exceeds 70 percent for 14 consecutive days. A storage expansion must be requested when used storage exceeds 80 percent of provisioned storage, or when the forecast predicts that it will exceed 80 percent within 30 days. Expansion requests are approved by the infrastructure budget owner and are normally fulfilled within 10 business days.

## 11. Service Decommissioning

A service may be decommissioned only after every dependent team has received at least 90 days' written notice. During the notice period the service remains fully supported. After shutdown, the service's data is archived for one year and then deleted, unless a legal hold applies. DNS records for the service are removed 30 days after shutdown, and the service's on-call rotation is closed on the day of shutdown.

## Appendix A. Lightweight Process

Services with fewer than 50 customers may deploy normal changes with approval from the service owner alone instead of the change advisory board, but they must still respect freeze windows. They may also replace the quarterly capacity forecast with a yearly one.
