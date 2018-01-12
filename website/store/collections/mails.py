from django.core.mail import EmailMessage
from django.template.loader import get_template


###Onderstaand zijn de emails voor als een klant een contact aanvraag indient###

#De contactRequestMail vangt de data van de klant op en roept vervolgens de specifieke functies aan#
def contactRequestMail(request):
    contact_name = request.POST.get('contact_name', '') #Pak de post variable en zet deze om naar Python variable
    contact_email = request.POST.get('contact_email', '')
    contact_content = request.POST.get('content', '')

    contactRequestAdminMail(contact_name, contact_email, contact_content)
    contactRequestCustomerMail(contact_name, contact_email, contact_content)

#De contactRequestAdminMail stuurt een mail naar de admin zodat zij het bericht in behandeling kunnen nemen#
def contactRequestAdminMail(contact_name, contact_email, contact_content):
    template = get_template('mail/contact_template.txt') #Fetch de email template
    context = {
        'contact_name': contact_name,
        'contact_email': contact_email,
        'contact_content': contact_content,
    }

    content = template.render(context) #Render de email

    email = EmailMessage(
        "Nieuwe contact aanvraag",
        content,
        'noreply@comicfire.com',
        ['admin@comicfire.com'],
        headers={'Reply-to': contact_email}
    )
    email.send() #Stuur de email

#De contactRequestCustomerMail stuurt een bevestiging naar de klant van hun bericht#
def contactRequestCustomerMail(contact_name, contact_email, contact_content):
    template = get_template('mail/contact_confirmation.txt')
    context = {
        'contact_name': contact_name,
        'contact_content': contact_content,
    }

    content = template.render(context)

    email = EmailMessage(
        "Uw bericht aan Comicfire",
        content,
        'noreply@comicfire.com',
        [contact_email]
    )
    email.send()

###Eind van mails van contact###

###Password reset door admin
def send_resetpassword_mail(user, newpw):
    template = get_template('mail/newpassword.txt')  # Fetch de email template
    context = {
        'contact_name': user.first_name,
        'contact_email': user.email,
        'contact_content': newpw,
    }

    content = template.render(context)  # Render de email

    email = EmailMessage(
        "Uw nieuwe wachtwoord",
        content,
        'noreply@comicfire.com',
        [user.email]
    )
    email.send()  # Stuur de email