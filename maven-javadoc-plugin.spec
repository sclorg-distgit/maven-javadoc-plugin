%global pkg_name maven-javadoc-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global bootstrap 0

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.9
Release:        8.14%{?dist}
Summary:        Maven Javadoc Plugin

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-javadoc-plugin
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip
Patch0:         reduce-exceptions.patch

BuildRequires:  %{?scl_prefix_java_common}apache-commons-io
BuildRequires:  %{?scl_prefix_java_common}apache-commons-lang
BuildRequires:  %{?scl_prefix_java_common}apache-commons-logging
BuildRequires:  %{?scl_prefix_java_common}jakarta-commons-httpclient
BuildRequires:  %{?scl_prefix_java_common}log4j
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-archiver
BuildRequires:  %{?scl_prefix}maven-artifact
BuildRequires:  %{?scl_prefix}maven-artifact-manager
BuildRequires:  %{?scl_prefix}maven-common-artifact-filters
BuildRequires:  %{?scl_prefix}maven-doxia-sink-api
BuildRequires:  %{?scl_prefix}maven-doxia-sitetools
BuildRequires:  %{?scl_prefix}maven-enforcer-plugin
BuildRequires:  %{?scl_prefix}maven-model
BuildRequires:  %{?scl_prefix}maven-plugin-annotations
BuildRequires:  %{?scl_prefix}maven-plugin-plugin
BuildRequires:  %{?scl_prefix}maven-plugin-testing-harness
BuildRequires:  %{?scl_prefix}maven-project
BuildRequires:  %{?scl_prefix}maven-resources-plugin
BuildRequires:  %{?scl_prefix}maven-settings
BuildRequires:  %{?scl_prefix}maven-shade-plugin
BuildRequires:  %{?scl_prefix}maven-invoker
BuildRequires:  %{?scl_prefix}maven-reporting-api
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-toolchain
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  %{?scl_prefix}modello
BuildRequires:  %{?scl_prefix}plexus-archiver
BuildRequires:  %{?scl_prefix}plexus-containers-container-default
BuildRequires:  %{?scl_prefix}plexus-interactivity-api
BuildRequires:  %{?scl_prefix}plexus-utils
BuildRequires:  %{?scl_prefix_java_common}qdox
%if ! %{bootstrap}
BuildRequires:  %{?scl_prefix}maven-javadoc-plugin
%endif


BuildArch: noarch

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.

%if ! %{bootstrap}
%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.
%endif

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Update source for use with newer doxia
%patch0

# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"

%pom_add_dep org.codehaus.plexus:plexus-interactivity-api pom.xml "
<exclusions>
    <exclusion>
        <groupId>org.codehaus.plexus</groupId>
        <artifactId>plexus-component-api</artifactId>
    </exclusion>
</exclusions>"

sed -i -e "s|org.apache.maven.doxia.module.xhtml.decoration.render|org.apache.maven.doxia.sink.render|g" src/main/java/org/apache/maven/plugin/javadoc/JavadocReport.java
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%if ! %{bootstrap}
%mvn_build -f
%else
# skip javadoc building
%mvn_build -fj
%endif
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE NOTICE

%if ! %{bootstrap}
%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE
%endif

%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.9-8.14
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.9-8.13
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.12
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.9-8.11
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.9-8.10
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.9
- Mass rebuild 2014-05-26

* Fri Feb 21 2014 Michael Simacek <msimacek@redhat.com> - 2.9-8.8
- plexus-interactivity split

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 2.9-8.7
- Adjust maven-wagon R/BR

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.5
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9-8
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9-7
- Migrate away from mvn-rpmbuild (#997429)

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-6
- Remove test dependencies from POM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.9-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-3
- Add missing requires
- Resolves: rhbz#893166

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9-2
- Add LICENSE and NOTICE files to packages (#879605)
- Add dependency exclusion to make enforcer happy

* Tue Oct 23 2012 Alexander Kurtakov <akurtako@redhat.com> 2.9-1
- Update to latest upstream version.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Alexander Kurtakov <akurtako@redhat.com> 2.8.1-1
- Update to latest upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Tomas Radej <tradej@redhat.com> - 2.8-4
- Added maven-compat dep to pom.xml

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-3
- Add BR on modello.

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-2
- FIx build in pure maven 3 environment.

* Wed May 11 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-1
- Update to latest upstream version.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 24 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-3
- Add missing invoker requires.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-2
- Add missing invoker BR.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-1
- Update to 2.7.

* Fri May  7 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-2
- Add jpackage-utils requirements
- Update requirements of javadoc subpackage

* Thu May  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-1
- Initial version, based on akurtakov's initial spec
