from support import Project


class Updates(Project):
    def test_repeat_init_preserves_learning_and_contract(self):
        self.initialize()
        overlay = self.project / "workspace/overlays/001.md"
        overlay.parent.mkdir()
        overlay.write_text("Learned taste", encoding="utf-8")
        with self.connection(self.db) as c:
            c.execute("INSERT INTO plans(id,title,status) VALUES (1,'Keep','active')")
            c.execute("INSERT INTO done_criteria(plan_id,criterion,passed,evidence) VALUES (1,'Keep',1,'tested')")
            c.execute("INSERT INTO rules(domain,key,value,source) VALUES ('design','taste','mine','overlay:001')")
            c.execute("UPDATE registry SET usage='user customization' WHERE name='shadcn/ui'")
            c.execute("INSERT INTO registry(kind,name,usage) VALUES ('tool','learned','keep')")
            c.execute("INSERT INTO design_guide_versions(path,kind) VALUES (?, 'overlay')", (str(overlay),))
            counts = c.execute("SELECT count(*) FROM rules WHERE source='core'").fetchone()
        self.initialize()
        self.initialize()
        with self.connection(self.db) as c:
            self.assertEqual(c.execute("SELECT count(*) FROM rules WHERE source='core'").fetchone(), counts)
            self.assertEqual(c.execute("SELECT usage FROM registry WHERE name='shadcn/ui'").fetchone()[0], "user customization")
            self.assertEqual(c.execute("SELECT passed,evidence FROM done_criteria").fetchone(), (1, "tested"))
            self.assertEqual(c.execute("SELECT value FROM rules WHERE source='overlay:001'").fetchone()[0], "mine")
            self.assertEqual(c.execute("SELECT count(*) FROM registry WHERE name='learned'").fetchone()[0], 1)
        self.assertEqual(overlay.read_text(), "Learned taste")

    def test_legacy_registry_preserved(self):
        self.initialize()
        with self.connection(self.db) as c:
            c.execute("DELETE FROM meta WHERE key LIKE 'seed:%'")
            c.execute("UPDATE registry SET usage='legacy edit' WHERE name='shadcn/ui'")
        self.initialize()
        with self.connection(self.db) as c:
            self.assertEqual(c.execute("SELECT usage FROM registry WHERE name='shadcn/ui'").fetchone()[0], "legacy edit")
