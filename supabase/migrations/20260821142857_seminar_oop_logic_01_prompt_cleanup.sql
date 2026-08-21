update public.learning_activity_variant_bank v
set prompt = regexp_replace(prompt, E' Pack [0-9]+\\.$', ''),
    updated_at = clock_timestamp()
from public.learning_activities a
where v.activity_id=a.id
  and a.slug='seminar11-oop-logic-01-2026'
  and v.checkpoint_key in ('Q10','Q11');
notify pgrst,'reload schema';
