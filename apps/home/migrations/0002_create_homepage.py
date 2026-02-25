from django.db import migrations


def create_homepage(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Page = apps.get_model("wagtailcore", "Page")
    Site = apps.get_model("wagtailcore", "Site")

    # Get content type for HomePage
    homepage_ct, _ = ContentType.objects.get_or_create(
        model="homepage",
        app_label="home",
    )

    # Get the default welcome page created by Wagtail
    try:
        welcome_page = Page.objects.get(depth=2, slug="home")
    except Page.DoesNotExist:
        welcome_page = Page.objects.get(depth=2)

    # Re-type the existing page to HomePage
    welcome_page.title = "Welcome to Wagtail!"
    welcome_page.content_type = homepage_ct
    welcome_page.save()

    # Create the HomePage-specific record via raw SQL to avoid ORM issues in migrations
    db_alias = schema_editor.connection.alias
    from django.db import connections

    with connections[db_alias].cursor() as cursor:
        cursor.execute(
            "INSERT INTO home_homepage (page_ptr_id, body) VALUES (%s, %s)",
            [
                welcome_page.pk,
                "<p>Your Wagtail site is running. Edit this page from the <a href='/admin/'>Wagtail admin</a>.</p>",
            ],
        )

    # Ensure the default Site points to our page
    Site.objects.update_or_create(
        is_default_site=True,
        defaults={
            "hostname": "localhost",
            "port": 80,
            "site_name": "Wagtail Starter",
            "root_page": welcome_page,
        },
    )


def remove_homepage(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    from django.db import connections

    with connections[db_alias].cursor() as cursor:
        cursor.execute("DELETE FROM home_homepage")


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
