import re


class Chain:
    def __init__(self):
        pass

    def extract_jobs(self, text):
        if not text or not text.strip():
            return []

        return [
            {
                "role": self._extract_role(text) or "Unknown role",
                "experience": self._extract_experience(text),
                "skills": self._extract_skills(text),
                "description": text.strip(),
            }
        ]

    def write_mail(self, job, links, company_name, recipient_role):
        role = job.get("role", "the role")
        skills = ", ".join(job.get("skills", []))
        skills_text = f"with experience in {skills}" if skills else "with a strong background relevant to this opportunity"

        portfolio_section = ""
        if links:
            portfolio_section = "\n\nRelevant portfolio examples:\n" + "\n".join(
                f"- {link}" for link in links
            )

        description = job.get("description", "").strip()
        summary = description[:600] + ("..." if len(description) > 600 else "")

        return (
            f"Hi {recipient_role},\n\n"
            f"I hope you are doing well. I am writing to express my interest in the {role} position at {company_name}. "
            f"I believe my background {skills_text} would make me a strong fit for this role.\n\n"
            f"In particular, I am drawn to this opportunity because of the strategic focus and the growth potential described in the job posting. "
            f"Below is a brief summary of how my experience aligns with the role:\n\n"
            f"{summary}\n\n"
            f"{portfolio_section}\n\n"
            f"I would welcome the opportunity to discuss how I can contribute to your team and support {company_name}'s goals. "
            f"Please let me know if you would like me to share additional details or schedule a time to talk.\n\n"
            f"Thank you for your consideration,\n\n"
            f"[Your Name]"
        )

    def _extract_role(self, text):
        patterns = [
            r"(?:Role|Position|Job Title)[:\-]\s*(.+)",
            r"^\s*(Senior|Junior|Lead|Principal)[^\n]+",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_skills(self, text):
        match = re.search(r"Skills?[:\-]\s*(.+)", text, flags=re.IGNORECASE)
        if match:
            skills = re.split(r",|;|\n", match.group(1))
            return [skill.strip() for skill in skills if skill.strip()]
        return []

    def _extract_experience(self, text):
        match = re.search(r"(\d+)\s+years?", text, flags=re.IGNORECASE)
        return match.group(0) if match else "N/A"
