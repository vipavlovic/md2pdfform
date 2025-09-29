# md2pdfform Comprehensive Feature Demo

This document demonstrates **all features** of md2pdfform, including every field type, markdown formatting, and advanced capabilities.

---

## Section 1: Text Input Fields

Standard text fields for collecting various types of information.

**Full Name:** {{text:full_name}}

**Address Line 1:** {{text:address_line_1}}

**Address Line 2:** {{text:address_line_2}}

**City:** {{text:city}}

---

## Section 2: Number and Email Fields

Specialized input types for numbers and email addresses.

**Age:** {{number:age}}

**Years of Experience:** {{number:years_experience}}

**Email Address:** {{email:primary_email}}

**Alternative Email:** {{email:secondary_email}}

---

## Section 3: Date Fields

Collect dates in a standardized format.

**Date of Birth:** {{date:birth_date}}

**Start Date:** {{date:start_date}}

**Expiration Date:** {{date:expiration_date}}

---

## Section 4: Checkbox Fields

Use checkboxes for yes/no or opt-in selections.

**I agree to the terms and conditions:** {{checkbox:terms_agreement}}

**Subscribe to newsletter:** {{checkbox:newsletter_subscription}}

**I am over 18 years old:** {{checkbox:age_verification}}

**Send me promotional emails:** {{checkbox:promotional_emails}}

**I have read the privacy policy:** {{checkbox:privacy_policy}}

---

## Section 5: Radio Button Groups

Radio buttons for mutually exclusive choices (2 options = radio buttons, 3+ = dropdown).

**Gender:** {{radio:gender:Male,Female}}

**Employment Status:** {{radio:employment:Full-time,Part-time}}

**T-Shirt Size:** {{radio:tshirt_size:Small,Medium,Large,X-Large}}

**Preferred Contact Method:** {{radio:contact_method:Email,Phone,SMS}}

---

## Section 6: Dropdown Menus

Dropdown menus for selecting from multiple options.

**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance,Operations,Legal}}

**Country of Residence:** {{dropdown:country:USA,Canada,UK,Australia,Germany,France,Japan,Other}}

**Education Level:** {{dropdown:education:High School,Associate Degree,Bachelor's Degree,Master's Degree,Doctorate,Other}}

**Industry:** {{dropdown:industry:Technology,Healthcare,Finance,Education,Manufacturing,Retail,Government,Non-Profit}}

---

## Section 7: Text Area Fields

Multi-line text areas with configurable line counts.

**Brief Bio (default 3 lines):**

{{textarea:brief_bio}}

**Detailed Project Description (5 lines):**

{{textarea:project_description:5}}

**Additional Comments (10 lines):**

{{textarea:additional_comments:10}}

**Feedback and Suggestions (7 lines):**

{{textarea:feedback:7}}

---

## Section 8: Multiple Fields Per Line

Place multiple form fields on the same line for compact layouts.

**First Name:** {{text:first_name}} **Last Name:** {{text:last_name}}

**Date:** {{date:event_date}} **Time:** {{text:event_time}}

**Hours:** {{number:hours}} **Minutes:** {{number:minutes}}

**Phone:** {{text:phone}} **Extension:** {{text:extension}}

**ZIP Code:** {{text:zip}} **Country Code:** {{text:country_code}}

---

## Section 9: Underscore Text Fields

Four or more underscores automatically convert to text input fields.

**Signature:** ________________________

**Printed Name:** ________________________

**Witness Signature:** ________________________

---

## Section 10: Markdown Formatting Features

### Heading Level 3

#### Heading Level 4

This paragraph contains **bold text** that appears inline with regular text. The **bold formatting is preserved** even when text wraps to multiple lines, which demonstrates the text wrapping capabilities of md2pdfform.

**This entire line is formatted in bold text.**

Here is a paragraph with normal text, followed by a **bold section in the middle**, and then more normal text at the end of the sentence.

---

## Section 11: Bullet Lists with Formatting

- First bullet point item
- Second item with **bold text** embedded
- Third item with a longer description that demonstrates how text wrapping works within list items
- Fourth item
- Fifth item with **multiple bold** sections and **additional formatting**

---

## Section 12: Horizontal Rules

You can create horizontal rules using three different syntaxes:

Three hyphens:

---

Three asterisks:

***

Three underscores:

___

All create visual separators in the document.

---

## Section 13: Mixed Content Example

This section demonstrates mixing various elements together.

### Personal Information

**Name:** {{text:participant_name}} **ID Number:** {{number:id_number}}

**Email:** {{email:contact_email}}

**Birth Date:** {{date:dob}} **Age:** {{number:current_age}}

### Preferences

**Communication Preference:** {{radio:comm_pref:Email,Phone}}

**Language:** {{dropdown:language:English,Spanish,French,German,Mandarin,Japanese}}

**Receive notifications:** {{checkbox:notifications}}

### Additional Details

**Please describe your experience and qualifications:**

{{textarea:experience:6}}

---

## Section 14: Long Text Wrapping Test

This is a very long paragraph designed to test the automatic text wrapping functionality of md2pdfform. It contains enough text to span multiple lines and demonstrates how the converter handles **bold text across line breaks** while maintaining proper formatting and readability. The system should automatically wrap this text to fit within the page margins without any manual intervention required from the user.

---

## Section 15: Complex Form Section

### Registration Form

**Full Legal Name:** {{text:legal_name}}

**Social Security Number:** {{text:ssn}} **Driver's License:** {{text:drivers_license}}

**Primary Phone:** {{text:primary_phone}} **Secondary Phone:** {{text:secondary_phone}}

**Email Address:** {{email:registration_email}}

**Street Address:** {{text:street_address}}

**City:** {{text:reg_city}} **State:** {{dropdown:state:AL,AK,AZ,AR,CA,CO,CT,DE,FL,GA,HI,ID,IL,IN,IA,KS,KY,LA,ME,MD,MA,MI,MN,MS,MO,MT,NE,NV,NH,NJ,NM,NY,NC,ND,OH,OK,OR,PA,RI,SC,SD,TN,TX,UT,VT,VA,WA,WV,WI,WY}}

**ZIP Code:** {{text:reg_zip}}

**Emergency Contact Name:** {{text:emergency_contact}} **Relationship:** {{text:emergency_relationship}}

**Emergency Phone:** {{text:emergency_phone}}

---

## Section 16: Survey Questions

**How satisfied are you with our service?**

{{radio:satisfaction:Very Satisfied,Satisfied,Neutral,Dissatisfied,Very Dissatisfied}}

**How likely are you to recommend us?**

{{dropdown:recommendation:Extremely Likely,Very Likely,Likely,Neutral,Unlikely,Very Unlikely,Extremely Unlikely}}

**What improvements would you suggest?**

{{textarea:improvements:8}}

**Would you like us to contact you about your feedback?** {{checkbox:contact_feedback}}

---

## Section 17: Date and Time Information

**Event Date:** {{date:event_date_final}}

**Registration Deadline:** {{date:registration_deadline}}

**Start Time:** {{text:start_time}} **End Time:** {{text:end_time}}

**Total Duration (hours):** {{number:duration_hours}}

---

## Section 18: Terms and Certification

I hereby certify that all information provided in this form is true and accurate to the best of my knowledge. I understand that providing false information may result in disqualification or termination.

**I certify the above statement:** {{checkbox:certification}}

**I agree to receive communications:** {{checkbox:communications_agreement}}

**I accept the privacy policy:** {{checkbox:privacy_acceptance}}

**I consent to background check:** {{checkbox:background_check}}

---

## Section 19: Signature Block

**Applicant Signature:** ________________________ **Date:** {{date:signature_date}}

**Printed Name:** ________________________

**Witness Name:** ________________________ **Witness Signature:** ________________________

**Witness Date:** {{date:witness_date}}

---

## Section 20: Final Notes

**Additional Notes or Comments:**

{{textarea:final_notes:5}}

---

**Thank you for completing this comprehensive demonstration form!**

This document has showcased all available features of md2pdfform including text fields, number fields, email fields, date fields, checkboxes, radio buttons, dropdown menus, text areas with custom line counts, multiple fields per line, underscore-to-field conversion, markdown formatting (bold text, headers, bullet points, horizontal rules), and proper text wrapping with page break handling.