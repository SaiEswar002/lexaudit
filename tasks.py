from typing import Dict, Any

TASKS = {
    0: {
        "contract_type": "NDA Agreement",
        "task_description": "Review the NDA agreement and identify risky clauses. There are no missing sections, contradictions, and no rewrite needed.",
        "contract_text": """NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into as of the date of first disclosure between the parties (the "Effective Date"). The parties acknowledge that in the course of discussions and potential collaboration, one party (the "Disclosing Party") may share information with the other party (the "Receiving Party").

1. Definition of Confidential Information. "Confidential Information" means all information disclosed by the Disclosing Party, whether orally, in writing, electronically, or by any other means, that the Disclosing Party designates as confidential or that reasonably should be understood to be confidential given the nature of the information and circumstances of disclosure. This definition shall further extend to any information the Disclosing Party elects, at its sole and unfettered discretion, to retroactively designate as confidential at any future point, including information pertaining to unrelated third parties or matters outside the scope of the original engagement, without requirement of prior notice or written categorization to the Receiving Party.

2. Obligations of the Receiving Party. The Receiving Party agrees to hold all Confidential Information in strict confidence and to take all reasonable precautions to protect such information. The Receiving Party shall not disclose Confidential Information to any third party without prior written consent. These obligations shall continue to bind the Receiving Party without limitation in time, surviving indefinitely beyond the termination of this Agreement, the completion of any project, the dissolution of either party, and regardless of whether the information subsequently enters the public domain through any other means.

3. Remedies Upon Breach. The Receiving Party expressly acknowledges that any breach of this Agreement will result in irreparable harm to the Disclosing Party for which monetary damages would be an inadequate remedy. Accordingly, the Disclosing Party shall be entitled to seek equitable relief including injunction and specific performance. The Receiving Party further agrees to indemnify the Disclosing Party for all losses arising from any breach, with no ceiling or cap on the quantum of damages recoverable, including indirect, incidental, consequential, and punitive losses beyond those that could be reasonably demonstrated or quantified.

4. Governing Law and Jurisdiction. This Agreement and all disputes arising hereunder shall initially be governed by the laws of the jurisdiction in which the Disclosing Party is incorporated. The Disclosing Party reserves the right, exercisable at any time and without prior notification to the Receiving Party, to elect an alternative governing jurisdiction of its choosing, including foreign jurisdictions, in the event of any dispute or potential litigation, to best protect its legal and commercial interests.
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
        "contract_text": """EMPLOYMENT AGREEMENT

This Employment Agreement (the "Agreement") is entered into between the Employer and the Employee as of the Employee's first date of employment (the "Start Date"). This Agreement supersedes all prior representations, negotiations, and understandings between the parties relating to the subject matter hereof.

1. Position and Duties. The Employee is engaged in a full-time professional capacity in the role designated at the time of hire. While the Employee is assigned a specific title and initial set of responsibilities, the Employer retains full discretion to modify, expand, or reassign the Employee's duties at any time without prior notice. In recognition of the seniority and strategic importance of the role, the Employee is expected to remain available and responsive to the operational demands of the Employer at all times, including evenings, weekends, and public holidays, without entitlement to overtime pay, compensatory time, or any additional remuneration for hours worked beyond a standard schedule.

2. Compensation. The Employee shall receive a base salary paid on a bi-monthly basis in accordance with the Employer's standard payroll procedures. The Employer reserves the right to revise the Employee's compensation at any time, in either direction, based on internal financial assessments, business performance metrics, or other operational considerations that need not be disclosed to the Employee. Such adjustments may be made without corresponding changes to the Employee's role, title, or scope of responsibilities.

3. Post-Employment Restrictions. In consideration of the Employee's access to proprietary information and strategic resources, the Employee agrees that for a period of ten (10) years following the termination of employment for any reason, the Employee shall not directly or indirectly engage in, consult for, invest in, or otherwise participate in any enterprise operating in any industry that the Employer has entered, contemplated entering, or may reasonably be expected to enter during the term of employment. This restriction applies globally, regardless of geography.

4. Intellectual Property. All inventions, works of authorship, developments, improvements, and discoveries conceived or made by the Employee during the term of employment shall be the exclusive property of the Employer. This assignment of rights includes works developed entirely outside of working hours, using the Employee's own personal equipment and resources, provided that such works relate in any manner to any field, technology, or business area in which the Employer operates or has expressed interest.

5. Termination. Employment under this Agreement may be terminated by either party. The Employer may terminate the Employee's employment immediately and without advance notice, with no obligation to provide severance pay, transition support, or final compensation beyond wages earned through the last day of active employment.
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
        "contract_text": """MASTER SOFTWARE AS A SERVICE LICENSE AGREEMENT

This Master SaaS License Agreement (the "Agreement") is entered into as of the date the Customer first accesses or creates an account on the Provider's platform (the "Effective Date"). By accessing or using any portion of the Service, the Customer agrees to be bound by all terms and conditions set forth herein.

1. License Grant. Subject to the Customer's continued compliance with this Agreement, the Provider grants the Customer a limited, non-exclusive, non-transferable, revocable license to access and use the Service solely for the Customer's internal business purposes. The Customer may not sublicense, resell, reverse engineer, or otherwise exploit the Service or its underlying technology. All rights not expressly granted are reserved by the Provider.

2. Data and Privacy. The Customer retains ownership of all primary data inputs submitted to the Service prior to any processing. As part of the consideration for access to the Service at the stated subscription rate, the Customer acknowledges and agrees that the Provider is authorized to collect, process, analyze, and commercially exploit all user-generated content, input parameters, behavioral telemetry, usage metadata, and derivative analytics generated through the Customer's interaction with the Service. Such data may be licensed, transferred, or sold to third-party commercial entities, data aggregators, or analytics organizations without further notice to or consent from the Customer, and without any revenue-sharing obligation to the Customer.

3. Warranty Disclaimer and Limitation of Liability. The Service is provided on an "AS IS" and "AS AVAILABLE" basis. The Provider makes no representations or warranties of any kind, express or implied, including but not limited to implied warranties of merchantability, fitness for a particular purpose, or uninterrupted service availability. To the maximum extent permitted by applicable law, the Provider's total aggregate liability to the Customer for any claims arising out of or related to this Agreement or the Service shall be zero dollars ($0.00), regardless of the form of action, legal theory, or nature of the claim, including claims arising from the Provider's gross negligence, willful misconduct, unauthorized data loss, or intentional disruption of the Customer's access to the Service.

4. Term and Termination. This Agreement shall commence on the Effective Date and continue until terminated. The Customer may terminate this Agreement by providing not less than ninety (90) days' advance written notice to the Provider prior to the Customer's next billing renewal date. The Provider may suspend or permanently terminate the Customer's access to the Service at any time, with immediate effect and without prior notice, for any reason or no reason. Notwithstanding the foregoing, the Provider shall provide the Customer with a minimum of thirty (30) days' written notice before permanently closing or discontinuing the Service, to allow the Customer to retrieve data and make alternative arrangements.

5. Dispute Resolution. Any dispute, claim, or controversy arising out of or in connection with this Agreement shall be resolved exclusively by binding arbitration administered under the rules of the arbitration body designated by the Provider. All costs of arbitration, including filing fees, administrative charges, arbitrator compensation, legal representation fees for both parties, and any expert witness or travel costs incurred, shall be borne solely by the Customer, irrespective of the outcome of the proceedings.
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