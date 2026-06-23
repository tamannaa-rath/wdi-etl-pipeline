# Architecture

> Status: stub. Fill in once the pipeline is actually running end-to-end and the diagram is drawn.

## TODO

- [ ] Full pipeline diagram (link from `docs/diagrams/pipeline-architecture.png`, built in Eraser.io)
- [ ] Bronze / Silver / Gold mapping table — what lives where, and why
- [ ] How chunked extraction handles the 3.6GB file (chunk size, memory reasoning)
- [ ] CI/CD flow: what triggers on push vs. what's manual vs. what's scheduled
- [ ] Local vs. cloud split: what runs on the team's machines vs. what runs in Supabase/Streamlit Cloud
- [ ] Secrets management (how DB credentials are handled between local and cloud)