## Step 4: Setup Django REST Framework, start the server, and test the API

> [!NOTE]
> **Behind the scenes:** This exercise uses custom instruction files that help guide GitHub Copilot's responses. The instruction file `.github/instructions/octofit_tracker_django_backend.instructions.md` contains Django REST Framework configuration, URL patterns, and API endpoint guidelines that Copilot references when generating code for this step.

In this step, we will accomplish the following:

- Setup the Django REST Framework.
- Start the server.
- Test the API using curl.

Copy and paste the following prompt(s) in the GitHub Copilot Chat and select the "Agent" instead of "Ask" or "Edit" from the drop down where you are inserting the prompt.

> [!TIP]
> - Keep in mind that the Copilot agent mode is conversational so it may ask you questions and you can ask it questions too.
> - Wait a moment for the Copilot to respond and press the continue button to execute commands presented by Copilot agent mode.
> - Keep files created and updated by Copilot agent mode until it is finished.
> - Agent mode has the ability to evaluate your code base and execute commands and add/refactor/delete parts of your code base and automatically self heal if it or you makes a mistake in the process.

**Open up a new Copilot Chat session by hitting the plus `+` icon in the Copilot Chat pane.**

### :keyboard: Activity: Setup Django REST Framework and test the REST API endpoints

> ![Static Badge](https://img.shields.io/badge/-Prompt-text?style=flat-square&logo=github%20copilot&labelColor=512a97&color=ecd8ff)
>
> ```prompt
> c
>```

> [!IMPORTANT]
> Don't start the Python Django app in the way that GitHub Copilot agent mode suggests hit
> **cancel**. Follow the next activity instead.

### :keyboard: Activity: Start the Python Django app and check the output

Now, let's actually try running the Django application! In the left sidebar, select the `Run and Debug` tab and then press the **Start Debugging** icon.

<img alt="Run Django" src="https://github.com/user-attachments/assets/a6c32898-bbeb-41ed-a8c5-488c8a42d507" width=30% height=30%>

Go to the running Django REST api url that pops up for port 8000 that looks like the following:

<img alt="django-rest-api-port" src="https://github.com/user-attachments/assets/627f3cbe-96ae-4a30-b38b-acd3cecf96ee" width=30% height=30%>

Once you open it in your web browser you will get a warning like the following:

<img alt="django-rest-api" src="https://github.com/user-attachments/assets/cb52d137-e78d-440b-8e9c-c322d7c49b48" width=30% height=30%>

Once you click `Continue` it should look similar the following with your codespace name:

<img alt="django-rest-api" src="https://github.com/user-attachments/assets/45ac98ba-aa7b-4953-81d6-e38bba97ae35" width=50% height=50%>

1. Now that we have updated our Django product to include our codespace name for the URL endpoint,
   let's check our changes in to our `build-octofit-app` branch.

1. With our new changes complete, please **commit** and **push** the changes to the `build-octofit-app` branch.

1. Wait a moment for Mona to check your work, provide feedback, and share the next lesson so we can keep working!

<details>
<summary>Having trouble? 🤷</summary><br/>

If you don't get feedback, here are some things to check:

- Make sure your commit changes were made for the following files to the branch `build-octofit-app` and pushed/synchronized to GitHub:
  - `octofit-tracker/backend/octofit_tracker/settings.py`
  - `octofit-tracker/backend/octofit_tracker/views.py`
- If Mona found a mistake, simply make a correction and push your changes again. Mona will check your work as many times as needed.

</details>
