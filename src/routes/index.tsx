import { createFileRoute } from "@tanstack/react-router";
import {
  Baby,
  Check,
  Clock3,
  ClipboardList,
  Heart,
  Moon,
  ShieldAlert,
  Sparkles,
  Syringe,
} from "lucide-react";

export const Route = createFileRoute("/")({ component: Home });

const chapters = [
  "First 24 hours, hour by hour",
  "A dedicated page for every month, 1 through 12",
  "What to feed, and what to skip",
  "Sleep expectations and a safe back-to-sleep routine",
  "Milestones and a simple activity for each month",
  "Vaccination reminder you can fill in",
  "Red flags: when to call the doctor",
  "Printable sleep log, shopping list, and emergency card",
];

const features = [
  {
    icon: Clock3,
    title: "First 24 hours",
    copy: "What happens right after birth, what to feed, and what not to put on newborn skin.",
  },
  {
    icon: Baby,
    title: "Month by month",
    copy: "Feeding, care, sleep, and milestones written so a tired parent can scan them.",
  },
  {
    icon: Moon,
    title: "Sleep, without myths",
    copy: "Realistic naps and nights, plus a one-week sleep log you can print.",
  },
  {
    icon: Syringe,
    title: "Vaccination card",
    copy: "A blank reminder to fill with dates from your own pediatrician.",
  },
  {
    icon: ShieldAlert,
    title: "When to call",
    copy: "Breathing trouble, fever, poor feeding, injury — clear reasons to seek care.",
  },
  {
    icon: ClipboardList,
    title: "Printable checklists",
    copy: "Shopping list, sleep log, vaccination tracker, and an emergency contact card.",
  },
];

const faqs = [
  {
    q: "Is this medical advice?",
    a: "No. It is a practical parent guide. Your pediatrician’s advice always comes first.",
  },
  {
    q: "How do I get the PDF?",
    a: "Tap Get the guide. Razorpay opens at ₹199. After payment, the PDF is delivered from that checkout.",
  },
  {
    q: "Can I print the checklists?",
    a: "Yes. The sleep log, shopping list, vaccination reminder, and emergency card are laid out for printing.",
  },
];

const PAY_URL = "https://pages.razorpay.com/pl_TbaGpu14FXQFy7/view";

function Home() {
  return (
    <div className="min-h-screen bg-cream text-ink">
      <header className="sticky top-0 z-20 border-b border-line bg-paper/90 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3">
          <a href="#top" className="font-display text-xl font-bold text-blue-deep">
            Cuddle<span className="text-pink">Nine</span>
          </a>
          <a
            href={PAY_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex rounded-full bg-pink px-4 py-2.5 text-sm font-extrabold text-paper shadow-sm"
          >
            Get the guide
          </a>
        </div>
      </header>

      <main id="top">
        <section className="bg-[linear-gradient(180deg,var(--color-blush),var(--color-sky)_55%,var(--color-cream))]">
          <div className="mx-auto grid max-w-5xl items-center gap-10 px-4 py-12 md:grid-cols-2 md:py-16">
            <div>
              <p className="mb-3 inline-flex items-center gap-2 rounded-full bg-paper px-3 py-1 text-sm font-bold text-pink">
                <Heart className="size-4" aria-hidden />
                Little Care, Big Love
              </p>
              <h1 className="font-display text-4xl font-bold leading-tight text-blue-deep md:text-5xl">
                Your baby’s first year, written down clearly.
              </h1>
              <p className="mt-4 max-w-md text-lg leading-relaxed text-muted">
                A 22-page illustrated guide for new parents: what to do, what to
                feed, and what to watch for from day one through month 12.
              </p>
              <div className="mt-6 flex flex-wrap items-center gap-3">
                <a
                  href={PAY_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex rounded-full bg-pink px-6 py-3 text-base font-extrabold text-paper"
                >
                  Get the PDF — ₹199
                </a>
                <p className="text-sm font-semibold text-muted">
                  <span className="line-through">₹999</span> Instant digital guide
                </p>
              </div>
            </div>

            <figure className="mx-auto w-full max-w-sm">
              <img
                src="/cover.jpg"
                alt="CuddleNine Complete 0 to 12 Months Baby Care Guide cover"
                className="w-full rounded-[1.4rem] shadow-[0_24px_50px_rgba(30,79,138,0.18)]"
              />
              <figcaption className="mt-3 text-center text-sm font-bold text-muted">
                22 pages · Instant PDF
              </figcaption>
            </figure>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-4 py-14">
          <h2 className="font-display text-3xl font-bold text-blue-deep">
            What the cover is promising
          </h2>
          <p className="mt-2 max-w-xl text-muted">
            That empty “22 Pages · Instant PDF” box was only a stand-in. This is
            the book parents actually open.
          </p>
          <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((item) => (
              <li
                key={item.title}
                className="rounded-card border border-line bg-paper p-5"
              >
                <item.icon className="size-5 text-blue" aria-hidden />
                <h3 className="mt-3 font-extrabold">{item.title}</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted">{item.copy}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="bg-paper">
          <div className="mx-auto grid max-w-5xl gap-8 px-4 py-14 md:grid-cols-2">
            <div>
              <h2 className="font-display text-3xl font-bold text-blue-deep">
                Inside the 22 pages
              </h2>
              <ul className="mt-6 space-y-3">
                {chapters.map((line) => (
                  <li key={line} className="flex gap-3 text-[15px] leading-snug">
                    <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full bg-pink text-paper">
                      <Check className="size-3" aria-hidden />
                    </span>
                    {line}
                  </li>
                ))}
              </ul>
            </div>
            <aside className="rounded-card bg-sky p-6">
              <Sparkles className="size-5 text-blue-deep" aria-hidden />
              <h3 className="mt-3 font-display text-2xl font-bold text-blue-deep">
                Made for the 2 a.m. question
              </h3>
              <p className="mt-3 leading-relaxed text-muted">
                Not a textbook. Short sections, illustrated pages, and a Mom’s
                Tip plus a “Call the Doctor” note on the monthly pages — so you
                know what is ordinary and what is not.
              </p>
              <p className="mt-4 rounded-2xl bg-paper px-4 py-3 text-sm font-semibold text-ink">
                Educational only. Always follow your pediatrician.
              </p>
            </aside>
          </div>
        </section>

        <section className="mx-auto max-w-3xl px-4 py-14">
          <h2 className="font-display text-3xl font-bold text-blue-deep">Questions</h2>
          <div className="mt-6 space-y-3">
            {faqs.map((item) => (
              <details
                key={item.q}
                className="rounded-card border border-line bg-paper px-5 py-4"
              >
                <summary className="cursor-pointer font-extrabold">{item.q}</summary>
                <p className="mt-2 text-sm leading-relaxed text-muted">{item.a}</p>
              </details>
            ))}
          </div>
        </section>

        <section className="px-4 pb-16">
          <div className="mx-auto max-w-3xl rounded-card bg-blue-deep px-6 py-10 text-center text-paper">
            <h2 className="font-display text-3xl font-bold">
              Start the first year with a plan.
            </h2>
            <p className="mx-auto mt-3 max-w-md text-sky">
              One payment. The full illustrated PDF. No subscription.
            </p>
            <a
              href={PAY_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-6 inline-flex rounded-full bg-paper px-6 py-3 font-extrabold text-pink-deep"
            >
              Pay ₹199
            </a>
          </div>
        </section>
      </main>

      <footer className="border-t border-line px-4 py-8 text-center text-sm text-muted">
        <p className="font-extrabold text-ink">CuddleNine · Little Care, Big Love</p>
        <p className="mt-1">Not a substitute for professional medical advice.</p>
      </footer>
    </div>
  );
}
