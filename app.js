const STORAGE_KEY = "nlp-practice-companion-state-v1";

const seedState = {
  currentUserId: null,
  currentView: {
    trainer: "dashboard",
    student: "dashboard",
  },
  users: [
    {
      id: "trainer-1",
      role: "trainer",
      firstName: "Sanne",
      lastName: "Vermeer",
      email: "trainer@nlpflow.app",
      password: "demo123",
      title: "Lead NLP Trainer",
      businessName: "Flow & Focus Coaching",
    },
    {
      id: "student-1",
      role: "student",
      firstName: "Mila",
      lastName: "de Jong",
      email: "mila@student.app",
      password: "demo123",
      trainerId: "trainer-1",
      programName: "Zelfvertrouwen Reset",
      startDate: "2026-03-10",
    },
    {
      id: "student-2",
      role: "student",
      firstName: "Jonas",
      lastName: "Bakker",
      email: "jonas@student.app",
      password: "demo123",
      trainerId: "trainer-1",
      programName: "Communicatie in Conflict",
      startDate: "2026-03-03",
    },
  ],
  exerciseTemplates: [
    {
      id: "tmpl-1",
      title: "Trigger Reflectie",
      category: "Bewustwording",
      objective: "Breng een terugkerende emotionele trigger in kaart.",
      instructions:
        "Beschrijf een recente situatie waarin je sterk reageerde. Onderzoek wat er gebeurde, welke gedachten opkwamen en wat je anders zou willen doen.",
      reflectionQuestions: [
        "Wat gebeurde er precies?",
        "Welke betekenis gaf je eraan?",
        "Wat zegt dit over je patroon?",
      ],
      estimatedMinutes: 15,
      difficulty: "Basis",
    },
    {
      id: "tmpl-2",
      title: "Outcome Frame",
      category: "Doelen",
      objective: "Maak je gewenste uitkomst concreet en aantrekkelijk.",
      instructions:
        "Werk je gewenste resultaat uit alsof het al haalbaar is. Beschrijf context, motivatie, bewijs van succes en eerste stap.",
      reflectionQuestions: [
        "Wat wil je precies bereiken?",
        "Waarom is dit belangrijk?",
        "Wat is je eerste kleine actie binnen 24 uur?",
      ],
      estimatedMinutes: 12,
      difficulty: "Basis",
    },
    {
      id: "tmpl-3",
      title: "Herkaderen van een Overtuiging",
      category: "Overtuigingen",
      objective: "Onderzoek een beperkende overtuiging en formuleer een bruikbare herformulering.",
      instructions:
        "Noteer een overtuiging die je klein houdt. Verzamel bewijs voor en tegen deze overtuiging en formuleer een realistischer alternatief.",
      reflectionQuestions: [
        "Welke overtuiging speelt hier?",
        "Welke feiten spreken dit tegen?",
        "Welke nieuwe overtuiging helpt je vooruit?",
      ],
      estimatedMinutes: 20,
      difficulty: "Verdieping",
    },
    {
      id: "tmpl-4",
      title: "Communicatie Check-in",
      category: "Communicatie",
      objective: "Bereid een belangrijk gesprek voor met intentie en helder taalgebruik.",
      instructions:
        "Denk aan een gesprek dat je wilt voeren. Beschrijf doel, gewenste sfeer, kernboodschap en welke state je wilt meenemen.",
      reflectionQuestions: [
        "Wat wil je dat de ander onthoudt?",
        "Welke emotionele state wil je vasthouden?",
        "Wat wordt je openingszin?",
      ],
      estimatedMinutes: 10,
      difficulty: "Basis",
    },
  ],
  assignments: [
    {
      id: "assign-1",
      templateId: "tmpl-1",
      studentId: "student-1",
      trainerId: "trainer-1",
      personalNote:
        "Kies een situatie uit deze week waarin je direct in de verdediging schoot.",
      dueDate: "2026-03-30",
      priority: "Hoog",
      status: "submitted",
      assignedAt: "2026-03-24T10:00:00Z",
    },
    {
      id: "assign-2",
      templateId: "tmpl-2",
      studentId: "student-1",
      trainerId: "trainer-1",
      personalNote:
        "Gebruik dit als voorbereiding op onze sessie van volgende week.",
      dueDate: "2026-04-03",
      priority: "Normaal",
      status: "assigned",
      assignedAt: "2026-03-27T11:00:00Z",
    },
    {
      id: "assign-3",
      templateId: "tmpl-4",
      studentId: "student-2",
      trainerId: "trainer-1",
      personalNote:
        "Focus op het gesprek met je teamlead en houd je taal concreet.",
      dueDate: "2026-03-29",
      priority: "Hoog",
      status: "in_progress",
      assignedAt: "2026-03-25T15:00:00Z",
    },
  ],
  submissions: [
    {
      id: "sub-1",
      assignmentId: "assign-1",
      answers: [
        "Ik voelde meteen spanning toen mijn collega mijn voorstel corrigeerde in de vergadering.",
        "Ik koppelde het aan de gedachte dat ik niet serieus genomen werd.",
        "Ik zie nu dat kritiek bij mij snel verandert in bewijs dat ik tekortschiet.",
      ],
      reflectionText:
        "Mijn automatische reactie was verdedigen. De volgende keer wil ik eerst vertragen en navragen wat de bedoeling is.",
      selfScore: 6,
      submittedAt: "2026-03-27T20:12:00Z",
      updatedAt: "2026-03-27T20:12:00Z",
    },
  ],
  feedback: [
    {
      id: "fb-1",
      submissionId: "sub-1",
      trainerId: "trainer-1",
      feedbackText:
        "Sterke observatie. In de volgende sessie wil ik met je oefenen hoe je spanning eerder in je lichaam herkent, zodat je voor het verdedigen al kunt vertragen.",
      createdAt: "2026-03-28T07:10:00Z",
    },
  ],
};

const app = document.getElementById("app");
let state = loadState();

function cloneSeedState() {
  return JSON.parse(JSON.stringify(seedState));
}

function createId(prefix) {
  if (window.crypto && typeof window.crypto.randomUUID === "function") {
    return `${prefix}-${window.crypto.randomUUID()}`;
  }
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 10)}`;
}

function loadState() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) {
    return cloneSeedState();
  }

  try {
    return JSON.parse(stored);
  } catch (error) {
    return cloneSeedState();
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function renderApp() {
  const currentUser = getCurrentUser();
  if (!currentUser) {
    renderLogin();
    return;
  }

  if (currentUser.role === "trainer") {
    renderTrainerApp(currentUser);
    return;
  }

  renderStudentApp(currentUser);
}

function getCurrentUser() {
  return state.users.find((user) => user.id === state.currentUserId) || null;
}

function fullName(user) {
  return `${user.firstName} ${user.lastName}`;
}

function getTemplate(templateId) {
  return state.exerciseTemplates.find((template) => template.id === templateId);
}

function getAssignment(assignmentId) {
  return state.assignments.find((assignment) => assignment.id === assignmentId);
}

function getSubmissionByAssignment(assignmentId) {
  return (
    state.submissions.find((submission) => submission.assignmentId === assignmentId) ||
    null
  );
}

function getFeedbackBySubmission(submissionId) {
  return state.feedback.filter((item) => item.submissionId === submissionId);
}

function formatDate(dateString) {
  return new Intl.DateTimeFormat("nl-NL", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(dateString));
}

function formatDateTime(dateString) {
  return new Intl.DateTimeFormat("nl-NL", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(dateString));
}

function isOverdue(assignment) {
  return (
    ["assigned", "in_progress"].includes(assignment.status) &&
    new Date(assignment.dueDate) < new Date("2026-03-28T23:59:59")
  );
}

function statusBadge(status, overdue) {
  const normalized = overdue ? "overdue" : status;
  const labels = {
    assigned: "Toegewezen",
    in_progress: "Bezig",
    submitted: "Ingediend",
    reviewed: "Beoordeeld",
    overdue: "Verlopen",
  };
  return `<span class="status ${normalized}">${labels[normalized]}</span>`;
}

function roleTabs(role) {
  const tabs =
    role === "trainer"
      ? [
          ["dashboard", "Dashboard"],
          ["students", "Studenten"],
          ["assign", "Toewijzen"],
          ["review", "Review"],
        ]
      : [
          ["dashboard", "Dashboard"],
          ["exercises", "Oefeningen"],
          ["progress", "Voortgang"],
          ["feedback", "Feedback"],
        ];

  return tabs
    .map(([id, label]) => {
      const active = state.currentView[role] === id ? "active" : "";
      return `<button class="nav-button ${active}" data-nav="${id}">${label}</button>`;
    })
    .join("");
}

function renderLayout(user, title, subtitle, mainContent, heroAside) {
  const roleLabel = user.role === "trainer" ? "Trainerruimte" : "Studentruimte";

  app.innerHTML = `
    <div class="app-shell">
      <aside class="sidebar">
        <div>
          <div class="brand-mark">NP</div>
          <h1 class="brand-title">NLP Practice Companion</h1>
          <p>${roleLabel} voor ritme, reflectie en opvolging tussen sessies.</p>
        </div>
        <div class="panel">
          <div class="top-strip">
            <div>
              <div class="tiny muted">${user.role === "trainer" ? "Ingelogd als trainer" : "Ingelogd als student"}</div>
              <strong>${fullName(user)}</strong>
            </div>
            <button class="button ghost" data-action="logout">Uitloggen</button>
          </div>
        </div>
        <nav class="nav">${roleTabs(user.role)}</nav>
        <div class="sidebar-footer tiny">
          Demoaccounts:
          <br />
          trainer@nlpflow.app / demo123
          <br />
          mila@student.app / demo123
          <br />
          jonas@student.app / demo123
        </div>
      </aside>

      <main class="content">
        <section class="hero-card">
          <div>
            <div class="hero-kicker">MVP prototype</div>
            <h2>${title}</h2>
            <p>${subtitle}</p>
            <div class="hero-actions">
              <button class="button primary" data-nav="${user.role === "trainer" ? "dashboard" : "exercises"}">Naar kernflow</button>
              <button class="button secondary" data-action="reset">Reset demo-data</button>
            </div>
          </div>
          <div class="panel">
            ${heroAside}
          </div>
        </section>

        ${mainContent}
      </main>
    </div>
  `;

  bindCommonEvents(user.role);
}

function bindCommonEvents(role) {
  document.querySelectorAll("[data-nav]").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentView[role] = button.dataset.nav;
      saveState();
      renderApp();
    });
  });

  document.querySelectorAll('[data-action="logout"]').forEach((button) => {
    button.addEventListener("click", () => {
      state.currentUserId = null;
      saveState();
      renderApp();
    });
  });

  document.querySelectorAll('[data-action="reset"]').forEach((button) => {
    button.addEventListener("click", () => {
      state = cloneSeedState();
      saveState();
      renderApp();
    });
  });
}

function renderLogin() {
  app.innerHTML = `
    <div class="login-shell">
      <section class="login-card">
        <div class="login-cover">
          <div class="hero-kicker" style="color: rgba(255,250,243,0.75);">Support tool voor NLP-trainers</div>
          <h1 class="serif">Begeleid groei tussen de sessies door.</h1>
          <p>
            Deze MVP laat de kern van het product zien: opdrachten toewijzen, reflecties verzamelen,
            voortgang volgen en feedback geven in een veilige, overzichtelijke flow.
          </p>
          <div class="demo-box">
            <strong>Wat deze demo al toont</strong>
            <p class="tiny">
              Trainerdashboard, studentdashboard, oefenbibliotheek, inzendingen, feedback en lokale opslag in de browser.
            </p>
          </div>
        </div>

        <div class="login-form">
          <div class="hero-kicker">Login</div>
          <h1>Welkom terug</h1>
          <p class="muted">Gebruik een van de demoaccounts om de trainer- of studentervaring te openen.</p>
          <form id="login-form" class="grid">
            <div class="field">
              <label for="email">E-mailadres</label>
              <input id="email" name="email" type="email" value="trainer@nlpflow.app" required />
            </div>
            <div class="field">
              <label for="password">Wachtwoord</label>
              <input id="password" name="password" type="password" value="demo123" required />
            </div>
            <button class="primary" type="submit">Inloggen</button>
          </form>
          <div class="panel" style="margin-top: 18px;">
            <strong>Demoaccounts</strong>
            <p class="tiny">Trainer: trainer@nlpflow.app / demo123</p>
            <p class="tiny">Student 1: mila@student.app / demo123</p>
            <p class="tiny">Student 2: jonas@student.app / demo123</p>
          </div>
          <p id="login-error" class="tiny" style="color: var(--danger);"></p>
        </div>
      </section>
    </div>
  `;

  document.getElementById("login-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const email = String(formData.get("email")).trim().toLowerCase();
    const password = String(formData.get("password")).trim();
    const user = state.users.find(
      (item) => item.email.toLowerCase() === email && item.password === password
    );

    if (!user) {
      document.getElementById("login-error").textContent =
        "Onbekende combinatie van e-mail en wachtwoord.";
      return;
    }

    state.currentUserId = user.id;
    saveState();
    renderApp();
  });
}

function renderTrainerApp(user) {
  const students = state.users.filter(
    (candidate) => candidate.role === "student" && candidate.trainerId === user.id
  );
  const assignments = state.assignments.filter((assignment) => assignment.trainerId === user.id);
  const submittedAssignments = assignments.filter((assignment) => assignment.status === "submitted");
  const overdueAssignments = assignments.filter((assignment) => isOverdue(assignment));
  const reviewedAssignments = assignments.filter((assignment) => assignment.status === "reviewed");
  const heroAside = `
    <h3>Coachingsmomenten die aandacht vragen</h3>
    <div class="list">
      <div class="list-item">
        <div class="list-item-header">
          <strong>In review</strong>
          <span class="pill submitted">${submittedAssignments.length}</span>
        </div>
        <p class="tiny">Inzendingen die op trainerfeedback wachten.</p>
      </div>
      <div class="list-item">
        <div class="list-item-header">
          <strong>Verlopen</strong>
          <span class="pill overdue">${overdueAssignments.length}</span>
        </div>
        <p class="tiny">Toegewezen oefeningen die nog niet zijn afgerond.</p>
      </div>
    </div>
  `;

  let content = "";
  switch (state.currentView.trainer) {
    case "students":
      content = renderTrainerStudents(students);
      break;
    case "assign":
      content = renderTrainerAssign(students);
      break;
    case "review":
      content = renderTrainerReview(user, students);
      break;
    default:
      content = renderTrainerDashboard(students, assignments, reviewedAssignments, overdueAssignments);
  }

  renderLayout(
    user,
    "Bewaak ritme, signaleer stilstand en geef feedback op het juiste moment.",
    "Deze trainerweergave focust op zakelijke waarde: snel toewijzen, zien wie vastloopt en persoonlijke opvolging geven zonder losse spreadsheets of chatgeschiedenis.",
    content,
    heroAside
  );

  bindTrainerEvents(user);
}

function renderTrainerDashboard(students, assignments, reviewedAssignments, overdueAssignments) {
  const completionRate = assignments.length
    ? Math.round(((reviewedAssignments.length + assignments.filter((item) => item.status === "submitted").length) / assignments.length) * 100)
    : 0;

  const studentCards = students
    .map((student) => {
      const items = state.assignments.filter((assignment) => assignment.studentId === student.id);
      const completed = items.filter((assignment) =>
        ["submitted", "reviewed"].includes(assignment.status)
      ).length;
      const nextDue = items
        .slice()
        .sort((left, right) => new Date(left.dueDate) - new Date(right.dueDate))[0];

      return `
        <div class="list-item">
          <div class="list-item-header">
            <div>
              <strong>${fullName(student)}</strong>
              <div class="tiny muted">${student.programName}</div>
            </div>
            <span class="pill ${completed === items.length && items.length ? "reviewed" : "assigned"}">${completed}/${items.length || 0}</span>
          </div>
          <p class="tiny">Volgende deadline: ${nextDue ? formatDate(nextDue.dueDate) : "Geen openstaande planning"}</p>
        </div>
      `;
    })
    .join("");

  const reviewList = assignments
    .filter((assignment) => assignment.status === "submitted" || isOverdue(assignment))
    .slice(0, 5)
    .map((assignment) => {
      const student = state.users.find((user) => user.id === assignment.studentId);
      const template = getTemplate(assignment.templateId);
      return `
        <div class="list-item">
          <div class="list-item-header">
            <div>
              <strong>${template.title}</strong>
              <div class="tiny muted">${fullName(student)}</div>
            </div>
            ${statusBadge(assignment.status, isOverdue(assignment))}
          </div>
          <p class="tiny">Deadline ${formatDate(assignment.dueDate)}</p>
        </div>
      `;
    })
    .join("");

  return `
    <section class="grid metrics-grid">
      <article class="metric-card">
        <div class="metric-label">Actieve studenten</div>
        <p class="metric-value">${students.length}</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Actieve opdrachten</div>
        <p class="metric-value">${assignments.length}</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Completion rate</div>
        <p class="metric-value">${completionRate}%</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Verlopen items</div>
        <p class="metric-value">${overdueAssignments.length}</p>
      </article>
    </section>

    <section class="grid two-col">
      <article class="panel">
        <div class="panel-header">
          <div>
            <h3>Studentmomentum</h3>
            <p class="muted">Wie beweegt, wie hapert en waar follow-up nodig is.</p>
          </div>
        </div>
        <div class="student-card-grid">
          ${studentCards || `<div class="empty-state">Nog geen studenten gekoppeld.</div>`}
        </div>
      </article>

      <article class="timeline-card">
        <div class="panel-header">
          <div>
            <h3>Actie nodig</h3>
            <p class="muted">Inzendingen en deadlines die aandacht vragen.</p>
          </div>
        </div>
        <div class="timeline">
          ${reviewList || `<div class="empty-state">Er wachten nu geen inzendingen op je.</div>`}
        </div>
      </article>
    </section>
  `;
}

function renderTrainerStudents(students) {
  const rows = students
    .map((student) => {
      const assignments = state.assignments.filter((assignment) => assignment.studentId === student.id);
      const completed = assignments.filter((assignment) =>
        ["submitted", "reviewed"].includes(assignment.status)
      ).length;
      const inReview = assignments.filter((assignment) => assignment.status === "submitted").length;
      return `
        <tr>
          <td>
            <strong>${fullName(student)}</strong>
            <div class="tiny muted">${student.programName}</div>
          </td>
          <td>${assignments.length}</td>
          <td>${completed}</td>
          <td>${inReview}</td>
          <td>${formatDate(student.startDate)}</td>
        </tr>
      `;
    })
    .join("");

  return `
    <section class="table-card">
      <div class="panel-header">
        <div>
          <h3>Studentenoverzicht</h3>
          <p class="muted">Eenvoudige tabel voor coachingspraktijken met kleine cohorten.</p>
        </div>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>Student</th>
            <th>Toegewezen</th>
            <th>Voltooid</th>
            <th>In review</th>
            <th>Start</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </section>
  `;
}

function renderTrainerAssign(students) {
  const studentOptions = students
    .map((student) => `<option value="${student.id}">${fullName(student)}</option>`)
    .join("");
  const templateOptions = state.exerciseTemplates
    .map(
      (template) =>
        `<option value="${template.id}">${template.title} · ${template.category} · ${template.estimatedMinutes} min</option>`
    )
    .join("");

  return `
    <section class="grid two-col">
      <article class="panel">
        <div class="panel-header">
          <div>
            <h3>Wijs een oefening toe</h3>
            <p class="muted">Trainer kiest student, template, deadline en persoonlijke context.</p>
          </div>
        </div>
        <form id="assign-form" class="grid">
          <div class="form-grid">
            <div class="field">
              <label for="studentId">Student</label>
              <select id="studentId" name="studentId" required>${studentOptions}</select>
            </div>
            <div class="field">
              <label for="templateId">Oefening</label>
              <select id="templateId" name="templateId" required>${templateOptions}</select>
            </div>
            <div class="field">
              <label for="dueDate">Deadline</label>
              <input id="dueDate" name="dueDate" type="date" value="2026-04-02" required />
            </div>
            <div class="field">
              <label for="priority">Prioriteit</label>
              <select id="priority" name="priority">
                <option>Normaal</option>
                <option>Hoog</option>
              </select>
            </div>
            <div class="field-full">
              <label for="personalNote">Persoonlijke context</label>
              <textarea id="personalNote" name="personalNote" placeholder="Welke situatie, doel of sessiecontext wil je meegeven?"></textarea>
            </div>
          </div>
          <div class="button-row">
            <button class="primary" type="submit">Toewijzen</button>
          </div>
        </form>
        <p id="assign-message" class="tiny muted"></p>
      </article>

      <article class="panel">
        <div class="panel-header">
          <div>
            <h3>Bibliotheek</h3>
            <p class="muted">Vaste MVP-templates die trainers snel kunnen hergebruiken.</p>
          </div>
        </div>
        <div class="list">
          ${state.exerciseTemplates
            .map(
              (template) => `
                <div class="exercise-card">
                  <div class="list-item-header">
                    <div>
                      <strong>${template.title}</strong>
                      <div class="tiny muted">${template.category} · ${template.difficulty}</div>
                    </div>
                    <span class="pill assigned">${template.estimatedMinutes} min</span>
                  </div>
                  <p>${template.objective}</p>
                  <p class="tiny">${template.instructions}</p>
                </div>
              `
            )
            .join("")}
        </div>
      </article>
    </section>
  `;
}

function renderTrainerReview(user, students) {
  const reviewAssignments = state.assignments
    .filter((assignment) => assignment.trainerId === user.id)
    .filter((assignment) => ["submitted", "reviewed"].includes(assignment.status))
    .sort((left, right) => {
      const leftSubmission = getSubmissionByAssignment(left.id);
      const rightSubmission = getSubmissionByAssignment(right.id);
      return new Date(rightSubmission?.submittedAt || 0) - new Date(leftSubmission?.submittedAt || 0);
    });

  const cards = reviewAssignments
    .map((assignment) => {
      const student = students.find((item) => item.id === assignment.studentId);
      const template = getTemplate(assignment.templateId);
      const submission = getSubmissionByAssignment(assignment.id);
      const feedbackItems = submission ? getFeedbackBySubmission(submission.id) : [];

      return `
        <article class="panel">
          <div class="panel-header">
            <div>
              <h3>${template.title}</h3>
              <p class="muted">${fullName(student)} · Ingeleverd op ${formatDateTime(submission.submittedAt)}</p>
            </div>
            ${statusBadge(assignment.status, false)}
          </div>
          <p><strong>Trainercontext:</strong> ${assignment.personalNote || "Geen extra toelichting."}</p>
          <div class="list">
            ${submission.answers
              .map(
                (answer, index) => `
                  <div class="answer-box">
                    <strong>Vraag ${index + 1}</strong>
                    <div class="tiny muted">${template.reflectionQuestions[index] || "Reflectie"}</div>
                    <p>${answer}</p>
                  </div>
                `
              )
              .join("")}
            <div class="answer-box">
              <strong>Reflectie</strong>
              <p>${submission.reflectionText}</p>
              <div class="tiny muted">Zelfscore: ${submission.selfScore}/10</div>
            </div>
          </div>
          <div class="list" style="margin-top: 18px;">
            ${feedbackItems.length
              ? feedbackItems
                  .map(
                    (item) => `
                      <div class="feedback-box">
                        <strong>Eerdere feedback</strong>
                        <p>${item.feedbackText}</p>
                        <div class="tiny muted">${formatDateTime(item.createdAt)}</div>
                      </div>
                    `
                  )
                  .join("")
              : `<div class="empty-state">Nog geen feedback toegevoegd.</div>`}
          </div>
          <form class="grid trainer-feedback-form" data-assignment-id="${assignment.id}">
            <div class="field">
              <label for="feedback-${assignment.id}">Nieuwe feedback</label>
              <textarea id="feedback-${assignment.id}" name="feedbackText" placeholder="Welke observatie, compliment of volgende stap geef je mee?" required></textarea>
            </div>
            <div class="button-row">
              <button class="primary" type="submit">Opslaan en markeren als beoordeeld</button>
            </div>
          </form>
        </article>
      `;
    })
    .join("");

  return cards || `<section class="panel"><div class="empty-state">Er zijn nog geen ingezonden oefeningen om te reviewen.</div></section>`;
}

function bindTrainerEvents(user) {
  const assignForm = document.getElementById("assign-form");
  if (assignForm) {
    assignForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData(assignForm);
      const nextAssignment = {
        id: createId("assign"),
        templateId: String(formData.get("templateId")),
        studentId: String(formData.get("studentId")),
        trainerId: user.id,
        personalNote: String(formData.get("personalNote")).trim(),
        dueDate: String(formData.get("dueDate")),
        priority: String(formData.get("priority")),
        status: "assigned",
        assignedAt: new Date().toISOString(),
      };

      state.assignments.unshift(nextAssignment);
      saveState();
      const target = document.getElementById("assign-message");
      target.textContent = "Oefening toegewezen. De student ziet deze direct in het dashboard.";
      assignForm.reset();
      document.getElementById("dueDate").value = "2026-04-02";
      renderApp();
    });
  }

  document.querySelectorAll(".trainer-feedback-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const assignmentId = form.dataset.assignmentId;
      const formData = new FormData(form);
      const feedbackText = String(formData.get("feedbackText")).trim();
      if (!feedbackText) {
        return;
      }

      const assignment = getAssignment(assignmentId);
      const submission = getSubmissionByAssignment(assignmentId);
      state.feedback.unshift({
        id: createId("fb"),
        submissionId: submission.id,
        trainerId: user.id,
        feedbackText,
        createdAt: new Date().toISOString(),
      });
      assignment.status = "reviewed";
      saveState();
      renderApp();
    });
  });
}

function renderStudentApp(user) {
  const assignments = state.assignments
    .filter((assignment) => assignment.studentId === user.id)
    .sort((left, right) => new Date(left.dueDate) - new Date(right.dueDate));
  const pending = assignments.filter((assignment) =>
    ["assigned", "in_progress"].includes(assignment.status)
  );
  const feedbackCount = assignments.reduce((count, assignment) => {
    const submission = getSubmissionByAssignment(assignment.id);
    if (!submission) {
      return count;
    }
    return count + getFeedbackBySubmission(submission.id).length;
  }, 0);
  const heroAside = `
    <h3>Jouw ritme</h3>
    <div class="bar-chart">
      <div class="bar-row">
        <strong>Openstaand</strong>
        <div class="bar-track"><div class="bar-fill" style="width: ${assignments.length ? (pending.length / assignments.length) * 100 : 0}%"></div></div>
        <span>${pending.length}</span>
      </div>
      <div class="bar-row">
        <strong>Feedback</strong>
        <div class="bar-track"><div class="bar-fill" style="width: ${Math.min(feedbackCount * 18, 100)}%"></div></div>
        <span>${feedbackCount}</span>
      </div>
    </div>
  `;

  let content = "";
  switch (state.currentView.student) {
    case "exercises":
      content = renderStudentExercises(user, assignments);
      break;
    case "progress":
      content = renderStudentProgress(user, assignments);
      break;
    case "feedback":
      content = renderStudentFeedback(assignments);
      break;
    default:
      content = renderStudentDashboard(assignments);
  }

  renderLayout(
    user,
    "Blijf in beweging tussen je sessies door, zonder te verdwalen in losse notities.",
    "Deze studentweergave draait om focus: weten wat nu belangrijk is, één oefening tegelijk afronden en terugzien welke groei al zichtbaar wordt.",
    content,
    heroAside
  );

  bindStudentEvents(user);
}

function renderStudentDashboard(assignments) {
  const next = assignments.find((assignment) => ["assigned", "in_progress"].includes(assignment.status));
  const completed = assignments.filter((assignment) =>
    ["submitted", "reviewed"].includes(assignment.status)
  ).length;
  const nextCard = next
    ? `
      <div class="exercise-card">
        <div class="list-item-header">
          <div>
            <strong>${getTemplate(next.templateId).title}</strong>
            <div class="tiny muted">Deadline ${formatDate(next.dueDate)}</div>
          </div>
          ${statusBadge(next.status, isOverdue(next))}
        </div>
        <p>${next.personalNote || getTemplate(next.templateId).objective}</p>
        <div class="button-row">
          <button class="button primary" data-student-open="${next.id}">Open oefening</button>
        </div>
      </div>
    `
    : `<div class="empty-state">Je hebt nu geen openstaande oefeningen. Mooi ritme.</div>`;

  return `
    <section class="grid metrics-grid">
      <article class="metric-card">
        <div class="metric-label">Openstaande oefeningen</div>
        <p class="metric-value">${assignments.filter((item) => ["assigned", "in_progress"].includes(item.status)).length}</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Afgerond</div>
        <p class="metric-value">${completed}</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Feedbackmomenten</div>
        <p class="metric-value">${assignments.reduce((count, assignment) => {
          const submission = getSubmissionByAssignment(assignment.id);
          return count + (submission ? getFeedbackBySubmission(submission.id).length : 0);
        }, 0)}</p>
      </article>
      <article class="metric-card">
        <div class="metric-label">Gem. zelfscore</div>
        <p class="metric-value">${averageSelfScore(assignments)}</p>
      </article>
    </section>

    <section class="grid two-col">
      <article class="panel">
        <div class="panel-header">
          <div>
            <h3>Volgende stap</h3>
            <p class="muted">De app laat eerst de meest logische actie zien.</p>
          </div>
        </div>
        ${nextCard}
      </article>
      <article class="timeline-card">
        <div class="panel-header">
          <div>
            <h3>Recente activiteit</h3>
            <p class="muted">Jouw laatste reflecties en feedbackmomenten.</p>
          </div>
        </div>
        <div class="timeline">
          ${renderActivityTimeline(assignments)}
        </div>
      </article>
    </section>
  `;
}

function renderStudentExercises(user, assignments) {
  const cards = assignments
    .map((assignment) => {
      const template = getTemplate(assignment.templateId);
      const submission = getSubmissionByAssignment(assignment.id);
      return `
        <article class="panel">
          <div class="panel-header">
            <div>
              <h3>${template.title}</h3>
              <p class="muted">${template.category} · ${template.estimatedMinutes} minuten</p>
            </div>
            ${statusBadge(assignment.status, isOverdue(assignment))}
          </div>
          <p><strong>Doel:</strong> ${template.objective}</p>
          <p>${template.instructions}</p>
          <div class="feedback-box">
            <strong>Persoonlijke noot van trainer</strong>
            <p>${assignment.personalNote || "Geen extra toelichting toegevoegd."}</p>
          </div>
          <div class="list">
            ${template.reflectionQuestions
              .map(
                (question, index) => `
                  <div class="answer-box">
                    <strong>Vraag ${index + 1}</strong>
                    <p>${question}</p>
                  </div>
                `
              )
              .join("")}
          </div>
          <form class="grid student-submission-form" data-assignment-id="${assignment.id}">
            ${template.reflectionQuestions
              .map(
                (question, index) => `
                  <div class="field">
                    <label for="answer-${assignment.id}-${index}">Antwoord ${index + 1}</label>
                    <textarea id="answer-${assignment.id}-${index}" name="answer-${index}" ${["submitted", "reviewed"].includes(assignment.status) ? "disabled" : ""}>${submission?.answers[index] || ""}</textarea>
                  </div>
                `
              )
              .join("")}
            <div class="field">
              <label for="reflection-${assignment.id}">Korte reflectie</label>
              <textarea id="reflection-${assignment.id}" name="reflectionText" ${["submitted", "reviewed"].includes(assignment.status) ? "disabled" : ""}>${submission?.reflectionText || ""}</textarea>
            </div>
            <div class="field">
              <label for="score-${assignment.id}">Zelfscore (1-10)</label>
              <input id="score-${assignment.id}" type="number" min="1" max="10" name="selfScore" value="${submission?.selfScore || 7}" ${["submitted", "reviewed"].includes(assignment.status) ? "disabled" : ""} />
            </div>
            ${
              ["submitted", "reviewed"].includes(assignment.status)
                ? `<div class="empty-state">Deze oefening is al ingestuurd. Feedback verschijnt in het tabblad Feedback.</div>`
                : `
                  <div class="button-row">
                    <button class="secondary" type="button" data-progress="${assignment.id}">Markeer als bezig</button>
                    <button class="primary" type="submit">Dien oefening in</button>
                  </div>
                `
            }
          </form>
        </article>
      `;
    })
    .join("");

  return cards || `<section class="panel"><div class="empty-state">Je hebt nog geen oefeningen ontvangen.</div></section>`;
}

function renderStudentProgress(user, assignments) {
  const categories = {};
  assignments.forEach((assignment) => {
    const template = getTemplate(assignment.templateId);
    categories[template.category] = categories[template.category] || { total: 0, complete: 0 };
    categories[template.category].total += 1;
    if (["submitted", "reviewed"].includes(assignment.status)) {
      categories[template.category].complete += 1;
    }
  });

  const bars = Object.entries(categories)
    .map(([category, data]) => {
      const percentage = data.total ? Math.round((data.complete / data.total) * 100) : 0;
      return `
        <div class="bar-row">
          <strong>${category}</strong>
          <div class="bar-track"><div class="bar-fill" style="width: ${percentage}%"></div></div>
          <span>${percentage}%</span>
        </div>
      `;
    })
    .join("");

  return `
    <section class="grid two-col">
      <article class="panel">
        <div class="panel-header">
          <div>
            <h3>Voortgang per thema</h3>
            <p class="muted">Eenvoudige MVP-metriek op basis van toegewezen en afgeronde oefeningen.</p>
          </div>
        </div>
        <div class="bar-chart">
          ${bars || `<div class="empty-state">Nog geen data om te tonen.</div>`}
        </div>
      </article>
      <article class="timeline-card">
        <div class="panel-header">
          <div>
            <h3>Persoonlijke samenvatting</h3>
            <p class="muted">Wat de app nu al kan teruggeven zonder complexe analytics.</p>
          </div>
        </div>
        <div class="list">
          <div class="list-item">
            <strong>Programma</strong>
            <p class="tiny">${user.programName}</p>
          </div>
          <div class="list-item">
            <strong>Gestart op</strong>
            <p class="tiny">${formatDate(user.startDate)}</p>
          </div>
          <div class="list-item">
            <strong>Gemiddelde zelfscore</strong>
            <p class="tiny">${averageSelfScore(assignments)} / 10</p>
          </div>
        </div>
      </article>
    </section>
  `;
}

function renderStudentFeedback(assignments) {
  const cards = assignments
    .map((assignment) => {
      const template = getTemplate(assignment.templateId);
      const submission = getSubmissionByAssignment(assignment.id);
      if (!submission) {
        return "";
      }

      const feedbackItems = getFeedbackBySubmission(submission.id);
      if (!feedbackItems.length) {
        return "";
      }

      return `
        <article class="panel">
          <div class="panel-header">
            <div>
              <h3>${template.title}</h3>
              <p class="muted">Feedback op jouw inzending</p>
            </div>
            ${statusBadge(assignment.status, false)}
          </div>
          <div class="list">
            ${feedbackItems
              .map(
                (item) => `
                  <div class="feedback-box">
                    <p>${item.feedbackText}</p>
                    <div class="tiny muted">${formatDateTime(item.createdAt)}</div>
                  </div>
                `
              )
              .join("")}
          </div>
        </article>
      `;
    })
    .join("");

  return cards || `<section class="panel"><div class="empty-state">Er is nog geen feedback beschikbaar. Rond eerst een oefening af.</div></section>`;
}

function bindStudentEvents(user) {
  document.querySelectorAll("[data-student-open]").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentView.student = "exercises";
      saveState();
      renderApp();
      setTimeout(() => {
        const form = document.querySelector(
          `.student-submission-form[data-assignment-id="${button.dataset.studentOpen}"]`
        );
        form?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 10);
    });
  });

  document.querySelectorAll("[data-progress]").forEach((button) => {
    button.addEventListener("click", () => {
      const assignment = getAssignment(button.dataset.progress);
      if (assignment && assignment.status === "assigned") {
        assignment.status = "in_progress";
        saveState();
        renderApp();
      }
    });
  });

  document.querySelectorAll(".student-submission-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const assignmentId = form.dataset.assignmentId;
      const assignment = getAssignment(assignmentId);
      const template = getTemplate(assignment.templateId);
      const formData = new FormData(form);
      const answers = template.reflectionQuestions.map((_, index) =>
        String(formData.get(`answer-${index}`)).trim()
      );
      const reflectionText = String(formData.get("reflectionText")).trim();
      const selfScore = Number(formData.get("selfScore"));

      if (answers.some((answer) => !answer) || !reflectionText || !selfScore) {
        return;
      }

      const existing = getSubmissionByAssignment(assignmentId);
      if (existing) {
        existing.answers = answers;
        existing.reflectionText = reflectionText;
        existing.selfScore = selfScore;
        existing.updatedAt = new Date().toISOString();
      } else {
        state.submissions.unshift({
          id: createId("sub"),
          assignmentId,
          answers,
          reflectionText,
          selfScore,
          submittedAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        });
      }

      assignment.status = "submitted";
      saveState();
      renderApp();
    });
  });
}

function renderActivityTimeline(assignments) {
  const items = [];
  assignments.forEach((assignment) => {
    const template = getTemplate(assignment.templateId);
    const submission = getSubmissionByAssignment(assignment.id);
    if (submission) {
      items.push({
        date: submission.submittedAt,
        title: `${template.title} ingediend`,
        body: `Zelfscore ${submission.selfScore}/10`,
      });

      getFeedbackBySubmission(submission.id).forEach((feedback) => {
        items.push({
          date: feedback.createdAt,
          title: `Feedback ontvangen op ${template.title}`,
          body: feedback.feedbackText,
        });
      });
    }
  });

  items.sort((left, right) => new Date(right.date) - new Date(left.date));

  if (!items.length) {
    return `<div class="empty-state">Je activiteit verschijnt hier zodra je een eerste oefening afrondt.</div>`;
  }

  return items
    .slice(0, 6)
    .map(
      (item) => `
        <div class="timeline-item">
          <strong>${item.title}</strong>
          <p>${item.body}</p>
          <div class="tiny muted">${formatDateTime(item.date)}</div>
        </div>
      `
    )
    .join("");
}

function averageSelfScore(assignments) {
  const scores = assignments
    .map((assignment) => getSubmissionByAssignment(assignment.id)?.selfScore)
    .filter(Boolean);
  if (!scores.length) {
    return "-";
  }
  return (scores.reduce((sum, score) => sum + score, 0) / scores.length).toFixed(1);
}

renderApp();
