from typing import Dict, Any

TASKS = {
    0: {
        "contract_type": "NDA Agreement",
        "task_description": "Review the NDA agreement and identify risky clauses. There are no missing sections, contradictions, and no rewrite needed.",
        "contract_text": """MUTUAL AND BINDING NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Mutual and Binding Non-Disclosure Agreement (the "Agreement") is formally entered into prior to any deep technical or business discussions by and between the Disclosing Party and the Receiving Party. The intent of this rigid document is to safeguard proprietary assets and trade secrets from unwarranted proliferation.

1. Expansive Definition of Confidential Information. Within the confines of this document, "Confidential Information" shall robustly mean any and all information disclosed verbally, electronically, visually, or in a physical written format during the course of the relationship. Furthermore, the definition of Confidential Information is not bounded by reasonable expectations; it includes not only the proprietary business strategies, algorithms, and product designs of the Disclosing Party, but explicitly covers any unrelated third-party info the Disclosing Party decides to add later, at its sole discretion, without providing prior written notice, categorization, or contextual relevance to the Receiving Party (overbroad_scope).

2. Rigorous Obligations of the Receiving Party. The Receiving Party agrees to use an incredibly high, near-absolute degree of care to protect the Confidential Information and prevent any unauthorized, accidental, or incidental use or disclosure. Distinct from standard industry practices that tether confidentiality to a period of relevance, these aggressive obligations of non-disclosure and restricted use shall survive in perpetuity and has no expiry date, remaining firmly in force regardless of the public availability of such information in the future or the dissolution of the parties involved (unlimited_confidentiality).

3. Immediate Remedies and Catastrophic Enforcement. The Receiving Party specifically acknowledges and concedes that any breach, whether minor or severe, intentional or accidental, of this Agreement will cause immediate, irreversible, and irreparable harm to the Disclosing Party. In any case of breach, the Receiving Party is reliable to unlimited penalties and the Disclosing Party can sue with no cap on damages. This punitive clause ensures that the Receiving Party could face financial ruin extending well beyond any demonstrable, mathematical economic loss, notwithstanding any statutory limitations or common law principles to the contrary (unlimited_penalties).

4. General Provisions and Jurisdictional Ambiguity. This Agreement constitutes the complete and entire agreement between the respective parties with respect to the subject matter hereof, merging all prior communications into this single enforceable entity. Initially, this agreement is governed by the laws of the State of incorporation, but the Disclosing Party forcefully reserves the right to change the governing law anytime without notice to any international or domestic jurisdiction of its choosing, specifically aiming to maximize operational advantage during any subsequent legal friction (changing_governing_law).
""",
        "expected_risks": [
            "unlimited_confidentiality",
            "unlimited_penalties",
            "overbroad_scope",
            "changing_governing_law"
        ],
        "expected_missing": [],
        "expected_contradictions": [],
        "expected_rewrite_clause": None
    },
    1: {
        "contract_type": "Employment Contract",
        "task_description": "Review the Employment Contract for risky clauses and missing sections.",
        "contract_text": """EXECUTIVE AND PROFESSIONAL EMPLOYMENT AGREEMENT

This Executive and Professional Employment Agreement (the "Agreement") is formed and made effective as of the official start date of the Employee. The parties mutually recognize that this document governs the totality of the employment relationship, superseding any prior verbal negotiations or written email communications.

1. Designation of Position, Duty Allocation, and Performance Expectations. The Employee shall serve in a comprehensive, full-time capacity for the Employer. The Employee is granted a specific job title, but the Employer retains the absolute prerogative to alter duties at will. Due to the high-stakes nature of the strategic role being offered, the Employee is required to have 24/7 availability with unlimited hours. This entails rendering services on weekends, public holidays, scheduled vacations, and late evenings as dictated by the Employer from time to time, without receiving any form of compensatory time off, overtime pay, or additional financial remuneration (unlimited_hours).

2. Remuneration, Taxation, and Compensation Adjustments. The Employee will be paid an attractive annual base salary, disbursed on a semi-monthly schedule according to the standard operating procedures of the Employer's payroll department. However, recognizing the turbulent economic climate and the necessity for extreme corporate financial flexibility, the Employer definitively reserves the right to change the salary anytime at their sole discretion. Such compensation alterations may be executed downwards without corresponding changes in role or responsibility, based on internal financial metrics not disclosed to the Employee (variable_salary).

3. Restrictive Covenants and Post-Employment Obligations. Recognizing the exceedingly sensitive and confidential nature of the Employer's business models, the Employee unequivocally agrees to be bound by an excessive non-compete clause, spanning 10 years worldwide after termination. During this expansive decade-long blackout period, the Employee may not engage, consult, or invest in any industry directly or indirectly related to any business vertical the Employer has ever considered entering, effectively rendering the Employee unable to work in their chosen profession (excessive_non_compete).

4. Discovery, Inventions, and Intellectual Property Rights. The Employer shall independently own all rights, title, and interest in any intellectual property, patents, trade secrets, or copyrighted material created by the Employee during the tenure of this contract. Going beyond the standard course of employment, the Employer claims overbroad IP ownership, including personal home projects done entirely on Employee's free time. This aggressive capture mechanism applies even if such personal projects were developed strictly using the Employee's personal equipment, resources, and independent knowledge without any relation to the Employer's primary business (overbroad_ip_ownership).

5. Term, Resignation, and Involuntary Termination. The employment relationship established herein is strictly at-will, granting enormous flexibility to the organization. The Employer can terminate this contract with no severance and zero notice, meaning employment can cease instantly upon verbal or written communication from management, leaving the Employee with no transition period or final payment guarantees (no_notice_termination).
""",
        "expected_risks": [
            "variable_salary",
            "unlimited_hours",
            "excessive_non_compete",
            "overbroad_ip_ownership",
            "no_notice_termination"
        ],
        "expected_missing": [
            "dispute_resolution",
            "benefits_and_leave"
        ],
        "expected_contradictions": [],
        "expected_rewrite_clause": None
    },
    2: {
        "contract_type": "SaaS License Agreement",
        "task_description": "Review the SaaS License Agreement for risks, missing sections, contradictions, and rewrite the zero_liability clause.",
        "contract_text": """MASTER SOFTWARE AS A SERVICE (SAAS) LICENSE AND SERVICE LEVEL AGREEMENT

This Master Software as a Service License and Service Level Agreement (this "Agreement") is entered into with binding effect as of the date of execution by the Customer (hereafter referred to as "Licensee", "User", or "Customer"). By initiating an account, logging into the application, or interacting with any endpoint on the Provider's proprietary cloud architecture platform (the "Service"), the Customer expressly and irrevocably accedes to all covenants, stipulations, guarantees, limitations, and conditions articulated herein or subsequently appended.

1. License Grant, Restrictions, and Extent of Permitted Usage. Subject strictly to the ongoing adherence to the terms delineated in this agreement, the Provider grants the Customer a geographically-limited, revocable, non-transferable, non-sublicensable, and non-exclusive mandate to deploy the Service internally. The Customer explicitly disclaims any rights to decompile, reverse engineer, scrape, mirror, or otherwise scrutinize the underlying algorithms, source code components, or database structures. The Customer must not deploy bots or automated agents that circumvent rate limits. 

2. Ownership of Data, Telemetry, Privacy, and Derived Information Vectors. Nothing in this document shall act backward to transfer pre-existing ownership of the Customer's primary data inputs prior to upload. However, as consideration for the heavily discounted transactional or market rate of the Service, the Provider is unconditionally authorized to engage in the continuous and pervasive user data resale. By this, it is explicitly understood that all inputted parameters, personal identifiers, system metadata, user telemetry actions, and derived analytics can be monetized, sub-licensed, or outright sold to unspecified third-party entities, data brokers, or intelligence organizations without any further explicit consent, notification, or profit-sharing obligations towards the Customer (user_data_resale).

3. Extent of Warranty, Implied Promises, and Complete Exculpation of Liability. All digital infrastructure, API endpoints, and storage repositories are proffered on a strictly "AS-IS" and "AS-AVAILABLE" methodology without warranties of merchantability or fitness for a particular niche purpose. The Customer agrees that under no circumstance, actionable event, or catastrophic failure shall the company owe any money. This absolute nullification of financial consequence, universally recognized as the zero liability parameter, asserts without ambiguity that the company owes $0 under any circumstance, no matter the damage, encompassing situations of extreme gross negligence, malicious insider attacks, total irreversible data deletion, or willful disruption affecting the Customer's downstream constituents (zero_liability).

4. Protocol for Cessation of Services, Suspension, and Notice Periods. Both parties possess administrative mechanisms to terminate the ongoing commercial engagement. To establish a predictable operational horizon and revenue forecasting for the Provider, this asymmetric termination protocol legally mandates that the user needs to provide 90 days of continuous, certified written notice of intent to cancel prior to their next billing cycle. In stark contrast to the Customer's obligations, the company needs 0 days to sever the relationship and lock the environment permanently and irrevocably (asymmetric_termination). Notwithstanding the previous sentence regarding immediate and unannounced cessation of access, the Provider commits that the company will, as an unalterable act of goodwill, always provide 30 days mandatory termination notice to the Customer's primary administrative contact before closing the service, allowing for adequate off-cycle data extraction (termination_notice_contradiction). 

5. Venue, Adjudication Parameters, and Equitable Relief. In the highly unlikely event that controversies or equitable claims surface from the performance or lack thereof under this complex commercial instrument, such matters must exclusively be brought before the specified arbitration tribunal located in the Provider's home jurisdiction. This dispute resolution architecture intentionally implements a strict forced cost bearing model, which incontrovertibly requires the user to pay all legal costs for both parties if a dispute arises, including expensive expert witness fees, travel costs, and administrative filing fees, completely circumventing traditional statutory 'loser-pays' provisions or standard split arbitration cost schemas (forced_cost_bearing).
""",
        "expected_risks": [
            "user_data_resale",
            "zero_liability",
            "asymmetric_termination",
            "forced_cost_bearing"
        ],
        "expected_missing": [
            "privacy_policy_reference",
            "refund_policy"
        ],
        "expected_contradictions": [
            "termination_notice_contradiction"
        ],
        "expected_rewrite_clause": "zero_liability"
    }
}

def get_task(task_id: int) -> Dict[str, Any]:
    if task_id not in TASKS:
        raise ValueError(f"Task ID {task_id} not found.")
    return TASKS[task_id]
