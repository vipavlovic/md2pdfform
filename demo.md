# md2pdfform Comprehensive Feature Demo

This document demonstrates **all features** of md2pdfform, including every field type, markdown formatting, and advanced capabilities.

---

## Section 1: Text Input Fields

Standard text fields for collecting various types of information.

**Full Name:** {{text:full_name::John Doe}}

**Address Line 1:** {{text:address_line_1::123 Main Street}}

**Address Line 2:** {{text:address_line_2::Apt 4B}}

**City:** {{text:city::San Francisco}}

---

## Section 2: Number and Email Fields

Specialized input types for numbers and email addresses.

**Age:** {{number:age::25}}

**Years of Experience:** {{number:years_experience::5}}

**Email Address:** {{email:primary_email::user@example.com}}

**Alternative Email:** {{email:secondary_email::alternate@example.com}}

---

## Section 3: Date Fields

Collect dates in a standardized format.

**Date of Birth:** {{date:birth_date::1990-01-15}}

**Start Date:** {{date:start_date::2024-01-01}}

**Expiration Date:** {{date:expiration_date::2025-12-31}}

---

## Section 4: Checkbox Fields

Use checkboxes for yes/no or opt-in selections.

**I agree to the terms and conditions:** {{checkbox:terms_agreement:true}}

**Subscribe to newsletter:** {{checkbox:newsletter_subscription:false}}

**I am over 18 years old:** {{checkbox:age_verification:true}}

**Send me promotional emails:** {{checkbox:promotional_emails:false}}

**I have read the privacy policy:** {{checkbox:privacy_policy:true}}

---

## Section 5: Radio Button Groups

Radio buttons for mutually exclusive choices (2 options = radio buttons, 3+ = dropdown).

**Gender:** {{radio:gender:Male,Female:Male}}

**Employment Status:** {{radio:employment:Full-time,Part-time:Full-time}}

**T-Shirt Size:** {{radio:tshirt_size:Small,Medium,Large,X-Large:Medium}}

**Preferred Contact Method:** {{radio:contact_method:Email,Phone,SMS:Email}}

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

{{textarea:brief_bio::I am a software engineer with a passion for creating user-friendly applications.}}

**Detailed Project Description (5 lines):**

{{textarea:project_description:5:This project involves developing a comprehensive form generation system that converts Markdown documents into interactive PDF forms with support for multiple field types and formatting options.}}

**Additional Comments (10 lines):**

{{textarea:additional_comments:10::}}

**Feedback and Suggestions (7 lines):**

{{textarea:feedback:7:Please provide your feedback on our service and any suggestions for improvement.}}

---

## Section 8: Multiple Fields Per Line

Place multiple form fields on the same line for compact layouts.

**First Name:** {{text:first_name:80:John}} **Last Name:** {{text:last_name:80:Smith}}

**Date:** {{date:event_date:100:2024-06-15}} **Time:** {{text:event_time:80:14:30}}

**Hours:** {{number:hours:60:2}} **Minutes:** {{number:minutes:60:30}}

**Phone:** {{text:phone:100:555-0123}} **Extension:** {{text:extension:60:101}}

**ZIP Code:** {{text:zip:80:94102}} **Country Code:** {{text:country_code:60:US}}

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

**Name:** {{text:participant_name::Jane Williams}} **ID Number:** {{number:id_number::12345}}

**Email:** {{email:contact_email::jane.williams@example.com}}

**Birth Date:** {{date:dob::1985-03-22}} **Age:** {{number:current_age::39}}

### Preferences

**Communication Preference:** {{radio:comm_pref:Email,Phone:Email}}

**Language:** {{dropdown:language:English,Spanish,French,German,Mandarin,Japanese}}

**Receive notifications:** {{checkbox:notifications:true}}

### Additional Details

**Please describe your experience and qualifications:**

{{textarea:experience:6:I have over 10 years of experience in software development, specializing in web applications and database design. I am proficient in Python, JavaScript, and SQL.}}

---

## Section 14: Long Text Wrapping Test

This is a very long paragraph designed to test the automatic text wrapping functionality of md2pdfform. It contains enough text to span multiple lines and demonstrates how the converter handles **bold text across line breaks** while maintaining proper formatting and readability. The system should automatically wrap this text to fit within the page margins without any manual intervention required from the user.

---

## Section 15: Complex Form Section

### Registration Form

**Full Legal Name:** {{text:legal_name::Robert James Anderson}}

**Social Security Number:** {{text:ssn:120:}} **Driver's License:** {{text:drivers_license:120:D1234567}}

**Primary Phone:** {{text:primary_phone:120:555-0100}} **Secondary Phone:** {{text:secondary_phone:120:555-0101}}

**Email Address:** {{email:registration_email::robert.anderson@example.com}}

**Street Address:** {{text:street_address::456 Oak Avenue}}

**City:** {{text:reg_city::Boston}} **State:** {{dropdown:state:AL,AK,AZ,AR,CA,CO,CT,DE,FL,GA,HI,ID,IL,IN,IA,KS,KY,LA,ME,MD,MA,MI,MN,MS,MO,MT,NE,NV,NH,NJ,NM,NY,NC,ND,OH,OK,OR,PA,RI,SC,SD,TN,TX,UT,VT,VA,WA,WV,WI,WY}}

**ZIP Code:** {{text:reg_zip::02101}}

**Emergency Contact Name:** {{text:emergency_contact::Mary Anderson}} **Relationship:** {{text:emergency_relationship::Spouse}}

**Emergency Phone:** {{text:emergency_phone::555-0102}}

---

## Section 16: Survey Questions

**How satisfied are you with our service?**

{{radio:satisfaction:Very Satisfied,Satisfied,Neutral,Dissatisfied,Very Dissatisfied:Satisfied}}

**How likely are you to recommend us?**

{{dropdown:recommendation:Extremely Likely,Very Likely,Likely,Neutral,Unlikely,Very Unlikely,Extremely Unlikely}}

**What improvements would you suggest?**

{{textarea:improvements:8:Consider adding more customization options and improving the mobile experience.}}

**Would you like us to contact you about your feedback?** {{checkbox:contact_feedback:yes}}

---

## Section 17: Date and Time Information

**Event Date:** {{date:event_date_final::2024-07-20}}

**Registration Deadline:** {{date:registration_deadline::2024-07-10}}

**Start Time:** {{text:start_time::09:00 AM}} **End Time:** {{text:end_time::05:00 PM}}

**Total Duration (hours):** {{number:duration_hours::8}}

---

## Section 18: Terms and Certification

I hereby certify that all information provided in this form is true and accurate to the best of my knowledge. I understand that providing false information may result in disqualification or termination.

**I certify the above statement:** {{checkbox:certification:true}}

**I agree to receive communications:** {{checkbox:communications_agreement:true}}

**I accept the privacy policy:** {{checkbox:privacy_acceptance:true}}

**I consent to background check:** {{checkbox:background_check:false}}

---

## Section 19: Signature Block

**Applicant Signature:** ________________________ **Date:** {{date:signature_date::2024-10-08}}

**Printed Name:** ________________________

**Witness Name:** ________________________ **Witness Signature:** ________________________

**Witness Date:** {{date:witness_date::}}

---

## Section 20: Code Block Demonstration

Code blocks are rendered in monospace font with a light gray background.

Here's an example Python function:

```
def calculate_total(items, tax_rate=0.08):
    """Calculate total price including tax"""
    subtotal = sum(item['price'] for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    return round(total, 2)

# Example usage
items = [
    {'name': 'Widget', 'price': 19.99},
    {'name': 'Gadget', 'price': 29.99}
]
total = calculate_total(items)
print(f"Total: ${total}")
```

Here's an example markdown form syntax:

```
# Contact Form Example

**Full Name:** {{text:contact_name::}}
**Email Address:** {{email:contact_email:250:}}
**Phone Number:** {{text:phone:120:555-1234}}
**Preferred Contact Time:** {{radio:contact_time:Morning,Afternoon,Evening:Afternoon}}
**Subscribe to updates:** {{checkbox:subscribe:true}}

**Message:**
{{textarea:message:5:400:Enter your message here}}
```

Code blocks preserve formatting and indentation, making them perfect for documentation and showing examples.

The Message would appear as this: {{textarea:message:5:400:Enter your message here}}

---

## Section 21: Final Notes

**Additional Notes or Comments:**

{{textarea:final_notes:5:This is a comprehensive demonstration of all md2pdfform features including default values for various field types.}}

---

**Thank you for completing this comprehensive demonstration form!**

This document has showcased all available features of md2pdfform including text fields, number fields, email fields, date fields, checkboxes, radio buttons, dropdown menus, text areas with custom line counts, multiple fields per line, underscore-to-field conversion, markdown formatting (bold text, headers, bullet points, horizontal rules), **code blocks with syntax preservation**, proper text wrapping with page break handling, and **default values** for all field types.